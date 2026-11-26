import sys
from pathlib import Path
sys.path.append(str(Path.resolve(Path(__file__).resolve().parent / '../RMpy package')))

import RMpy.common as RMc       # noqa #type: ignore
import RMpy.launcher            # noqa #type: ignore

import configparser
import re
import xml.etree.ElementTree as ET

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v12
#   Python for Windows v3.15

# Config files fields used
#    FILE_PATHS  DB_PATH
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#    FILE_PATHS  RMNOCASE_PATH
#    FILE_PATHS  REGEXP_PATH

#    FILTER   SOURCE_TEMPLATE
#    FILTER   SOURCE_NAME
#    FILTER   CITATION_NAME
#    FILTER   USE_REGEXP

#   CITATION_NAME_UPDATER  MAKE_CHANGES
#   CITATION_NAME_UPDATER  TEMPLATE_DEFAULT
#   CITATION_NAME_UPDATER  TEMPLATE_FROM_SOURCE_TEMPLATE
#   CITATION_NAME_UPDATER  CUSTOM_TEMPLATE


# ===================================================DIV60==
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"]      = "CitationNameUpdater"
    utility_info["utility_version"] = "UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE"
    utility_info["config_file_name"]  = "RM-Python-config.ini"
    utility_info["script_path"]  = Path(__file__).parent
    utility_info["run_features_function"]  = run_update_citation_name
    utility_info["allow_db_changes"]  = True
    utility_info["RMNOCASE_required"] = True
    utility_info["RMNOCASE_optional"] = False
    utility_info["RegExp_required"]   = False
    utility_info["RegExp_optional"]   = True


    RMpy.launcher.launcher(utility_info)


# ===================================================DIV60==
def run_update_citation_name(config, db_connection, report_file):

    # deal with RMNOCASE used to collateCitationTable.CitationName
    # and issue a warning in report to check DB integrity in RM.
    RMc.reindex_RMNOCASE(db_connection)

    use_regexp = RMc.get_bool_option(config, "FILTER", "USE_REGEXP")
    make_changes = RMc.get_bool_option(config, "CITATION_NAME_UPDATER", "MAKE_CHANGES")
    template_default = RMc.get_bool_option(
        config, "CITATION_NAME_UPDATER", "TEMPLATE_DEFAULT")

    if template_default:
        template_from_source_template = False
        custom_template = ""
    else:
        template_from_source_template = RMc.get_bool_option(
            config, "CITATION_NAME_UPDATER", "TEMPLATE_FROM_SOURCE_TEMPLATE")
        try:
            custom_template = config["CITATION_NAME_UPDATER"]["CUSTOM_TEMPLATE"]
        except (configparser.Error, KeyError) as exc:
            raise RMc.RM_Py_Exception(
                "ERROR: [CITATION_NAME_UPDATER] CUSTOM_TEMPLATE must be specified."
            ) from exc

    try:
        source_template_filter = RMc.get_unquoted_value(
            config.get("FILTER", "SOURCE_TEMPLATE", fallback=""))
        source_name_filter = RMc.get_unquoted_value(
            config.get("FILTER", "SOURCE_NAME", fallback=""))
        citation_name_filter = RMc.get_unquoted_value(
            config.get("FILTER", "CITATION_NAME", fallback=""))
    except configparser.Error as exc:
        raise RMc.RM_Py_Exception(
            "ERROR: The [FILTER] configuration section is missing.") from exc

    if use_regexp:
        try:
            db_connection.execute("SELECT '' WHERE '' REGEXP ''")
        except Exception as exc:
            raise RMc.RM_Py_Exception(
                "ERROR: REGEXP extension was not loaded. "
                "Verify REGEXP_PATH is configured and points to a valid extension file.") from exc

    from_clause = """
        FROM CitationTable AS ct
        JOIN SourceTable AS s ON s.SourceID = ct.SourceID
        LEFT JOIN SourceTemplateTable AS st ON st.TemplateID = s.TemplateID
    """
    filter_conditions = []
    filter_parameters = []

    def count_citations(extra_condition="", extra_parameters=()):
        conditions = list(filter_conditions)
        parameters = list(filter_parameters)
        if extra_condition:
            conditions.append(extra_condition)
            parameters.extend(extra_parameters)
        where_clause = (
            " WHERE " + " AND ".join(conditions) if conditions else "")
        cursor = db_connection.execute(
            "SELECT COUNT(*) " + from_clause + where_clause, parameters)
        return cursor.fetchone()[0]

    if make_changes:
        report_file.write(
            "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
            "IMPORTANT:\n"
            "  Be sure to run the RootsMagic database tool:\n"
            " 'Integrity check' when a modified database is first\n"
            "  opened in RootsMagic. Select the tool 'Rebuild indexes'\n"
            "  if the check returns anything but 'ok'.\n"
            "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
            "\n\n")

    report_file.write(
        "+=+=+=+= Citation name filters\n"
        f"Mode: {'update database' if make_changes else 'preview only'}\n")
    remaining = count_citations()

    if source_template_filter:
        before_filter = remaining
        if use_regexp:
            condition = "st.Name REGEXP ?"
            parameters = (source_template_filter,)
            matched = count_citations(condition, parameters)
            description = "regular expression"
        else:
            template_ids = db_connection.execute(
                "SELECT TemplateID FROM SourceTemplateTable "
                "WHERE Name COLLATE BINARY = ?",
                (source_template_filter,)).fetchall()
            report_file.write(
                f"SOURCE_TEMPLATE exact name {source_template_filter!r}: "
                f"{len(template_ids)} templates found.\n")
            if len(template_ids) != 1:
                reason = "not found" if not template_ids else "not unique"
                raise RMc.RM_Py_Exception(
                    f"ERROR: SOURCE_TEMPLATE {source_template_filter!r} "
                    f"was {reason}.")
            condition = "st.TemplateID = ?"
            parameters = (template_ids[0][0],)
            matched = count_citations(condition, parameters)
            description = "exact name"
        filter_conditions.append(condition)
        filter_parameters.extend(parameters)
        remaining = count_citations()
        report_file.write(
            f"SOURCE_TEMPLATE ({description}): {before_filter} before filter, "
            f"{matched} matched after prior filters; "
            f"{remaining} remain after intersection.\n")
    else:
        report_file.write(
            f"SOURCE_TEMPLATE: (blank - not applied); {remaining} citations remain.\n")

    if source_name_filter:
        before_filter = remaining
        if use_regexp:
            condition = "s.Name REGEXP ?"
            parameters = (source_name_filter,)
            matched = count_citations(condition, parameters)
            description = "regular expression"
        else:
            source_ids = db_connection.execute(
                "SELECT SourceID FROM SourceTable "
                "WHERE Name COLLATE BINARY = ?",
                (source_name_filter,)).fetchall()
            report_file.write(
                f"SOURCE_NAME exact name {source_name_filter!r}: "
                f"{len(source_ids)} sources found.\n")
            if len(source_ids) != 1:
                reason = "not found" if not source_ids else "not unique"
                raise RMc.RM_Py_Exception(
                    f"ERROR: SOURCE_NAME {source_name_filter!r} was {reason}.")
            condition = "s.SourceID = ?"
            parameters = (source_ids[0][0],)
            matched = count_citations(condition, parameters)
            description = "exact name"
        filter_conditions.append(condition)
        filter_parameters.extend(parameters)
        remaining = count_citations()
        report_file.write(
            f"SOURCE_NAME ({description}): {before_filter} before filter, "
            f"{matched} matched after prior filters; "
            f"{remaining} remain after intersection.\n")
    else:
        report_file.write(
            f"SOURCE_NAME: (blank - not applied); {remaining} citations remain.\n")

    if citation_name_filter:
        before_filter = remaining
        if use_regexp:
            condition = "ct.CitationName REGEXP ?"
            parameters = (citation_name_filter,)
            matched = db_connection.execute(
                "SELECT COUNT(*) FROM CitationTable AS ct "
                "WHERE ct.CitationName REGEXP ?", parameters).fetchone()[0]
            description = "regular expression"
        else:
            condition = "ct.CitationName COLLATE BINARY = ?"
            parameters = (citation_name_filter,)
            matched = db_connection.execute(
                "SELECT COUNT(*) FROM CitationTable AS ct "
                "WHERE ct.CitationName COLLATE BINARY = ?", parameters
            ).fetchone()[0]
            description = "exact name"
        if matched == 0:
            raise RMc.RM_Py_Exception(
                f"ERROR: CITATION_NAME {citation_name_filter!r} was not found.")
        filter_conditions.append(condition)
        filter_parameters.extend(parameters)
        remaining = count_citations()
        report_file.write(
            f"CITATION_NAME ({description}): {before_filter} before filter, "
            f"{matched} matched after prior filters; "
            f"{remaining} remain after intersection.\n")
    else:
        report_file.write(
            f"CITATION_NAME: (blank - not applied); {remaining} citations remain.\n")

    # Count distinct source templates and sources
    where_clause = (
        " WHERE " + " AND ".join(filter_conditions)
        if filter_conditions else "")

    distinct_templates = db_connection.execute(
        "SELECT COUNT(DISTINCT st.TemplateID) " + from_clause + where_clause,
        filter_parameters).fetchone()[0]

    distinct_sources = db_connection.execute(
        "SELECT COUNT(DISTINCT s.SourceID) " + from_clause + where_clause,
        filter_parameters).fetchone()[0]

    report_file.write(
        f"Source templates: {distinct_templates}\n"
        f"Sources: {distinct_sources}\n"
        f"Selected citations: {remaining}\n")

    source_template_columns = {
        row[1] for row in db_connection.execute(
            "PRAGMA table_info(SourceTemplateTable)").fetchall()
    }
    has_template_citation_name = "CitationName" in source_template_columns
    if template_from_source_template and not has_template_citation_name:
        raise RMc.RM_Py_Exception(
            "ERROR: SourceTemplateTable.CitationName is not available in this "
            "RootsMagic database.")
    source_template_citation_name_column = (
        "st.CitationName" if has_template_citation_name else "''")

    selected_where = (
        " WHERE " + " AND ".join(filter_conditions)
        if filter_conditions else "")
    selected_rows = db_connection.execute(
        """
        SELECT ct.CitationID, ct.CitationName, ct.Fields, s.TemplateID,
               """ + source_template_citation_name_column +
        """, st.FieldDefs, st.Name, s.Name, s.SourceID
        """ + from_clause + selected_where +
        " ORDER BY s.TemplateID, s.Name, ct.CitationID", filter_parameters).fetchall()

    def parse_xml_fields(xml_data, field_name, record_description):
        if xml_data in (None, b"", ""):
            return {}
        try:
            root = ET.fromstring(xml_data)
        except (ET.ParseError, TypeError, ValueError) as exc:
            raise RMc.RM_Py_Exception(
                f"ERROR: Invalid {field_name} XML for {record_description}."
            ) from exc
        fields = {}
        for field in root.findall("./Fields/Field"):
            name = field.findtext("Name")
            if name is None:
                name = field.findtext("FieldName")
            if name:
                value_element = field.find("Value")
                if value_element is not None:
                    fields[name.casefold()] = value_element.text or ""
        return fields

    def parse_field_definitions(xml_data, record_description):
        if xml_data in (None, b"", ""):
            return {}
        try:
            root = ET.fromstring(xml_data)
        except (ET.ParseError, TypeError, ValueError) as exc:
            raise RMc.RM_Py_Exception(
                f"ERROR: Invalid FieldDefs XML for {record_description}.") from exc
        definitions = {}
        for field in root.findall("./Fields/Field"):
            name = field.findtext("FieldName")
            if not name or (field.findtext("CitationField") or "").casefold() not in (
                    "true", "1"):
                continue
            definitions[name.casefold()] = (
                name, (field.findtext("Type") or "").casefold())
        return definitions

    template_data = {}
    citations_missing_template = []

    # Build template_data from selected_rows (index 3=s.TemplateID, 5=st.FieldDefs, 6=st.Name)
    for (citation_id, _, _, template_id, _, field_defs_xml,
         template_name, _, _) in selected_rows:
        if template_id is None:
            citations_missing_template.append(citation_id)
            continue

        if template_id not in template_data:
            definitions = parse_field_definitions(
                field_defs_xml, f"source template {template_id}")
            default_template = "; ".join(
                f"[{name}]" for name, _ in definitions.values())

            # Template ID 0 means free-form source
            if template_id == 0:
                display_name = "FREE-FORM SOURCE (No Template)"
            else:
                display_name = template_name if template_name else f"Template {template_id}"

            template_data[template_id] = (
                display_name, definitions, default_template)

    report_file.write("\n+=+=+=+= Default templates for SourceTemplate used by selected citations\n")
    if not template_data:
        report_file.write("No source templates selected.\n")
    else:
        report_file.write(f"Found {len(template_data)} source template(s)\n")
    for template_id in sorted(template_data.keys()):
        template_name, _, default_template = template_data[template_id]
        report_file.write(
            f"\nSource template {template_id}: {template_name}\n"
            f"{default_template}\n\n")

    if not template_default and not template_from_source_template and len(template_data) > 1:
        raise RMc.RM_Py_Exception(
            "ERROR: CUSTOM_TEMPLATE requires all selected citations to "
            "use the same source template. No changes were made.")

    changes = []
    unresolved_fields = {}  # Track unresolved fields by template/source/field

    for (citation_id, old_name, citation_fields_xml, template_id,
         source_template_citation_name, _, _, source_name, source_id) in selected_rows:
        if template_id is None:
            continue
        _, definitions, default_template = template_data[template_id]
        citation_fields = parse_xml_fields(
            citation_fields_xml, "Citation Fields", f"citation {citation_id}")

        if template_default:
            template = default_template
        elif template_from_source_template:
            template = source_template_citation_name or ""
        else:
            template = custom_template

        def substitute_field(match):
            field_name = match.group(1)
            field_key = field_name.casefold()
            if field_key in definitions and field_key in citation_fields:
                return citation_fields[field_key]
            # Track unresolved fields: either not in definitions OR missing from citation
            if field_key not in definitions or field_key not in citation_fields:
                template_name = template_data[template_id][0]
                key = (template_name, source_name, field_name, citation_id)
                if key not in unresolved_fields:
                    unresolved_fields[key] = {
                        'template_name': template_name,
                        'source_name': source_name,
                        'field_name': field_name,
                        'citation_ids': []
                    }
                if citation_id not in unresolved_fields[key]['citation_ids']:
                    unresolved_fields[key]['citation_ids'].append(citation_id)
            return match.group(0)

        new_name = re.sub(r"\[([^\[\]]+)\]", substitute_field, template)
        changes.append((citation_id, old_name or "", new_name, template_id, source_name))

    report_file.write(
        "\n+=+=+=+= Citation name changes listing\n\n"
        "Key:\n"
        "Citation number\nOld CitationName\nNew CitationName\n\n")

    updated = 0
    current_template = None
    current_source = None

    for citation_id, old_name, new_name, template_id, source_name in changes:
        template_name = template_data[template_id][0]

        if current_template != template_name:
            current_template = template_name
            current_source = None
            report_file.write(
                f"\n--- Source Template Name: {template_name} ---\n\n")

        if current_source != source_name:
            current_source = source_name
            report_file.write(
                f"--  Source Name: {source_name}\n\n")

        report_file.write(
            f"  {citation_id}\n"
            f"  {old_name!r}\n"
            f"  {new_name!r}\n\n")
        if make_changes and old_name != new_name:
            db_connection.execute(
                "UPDATE CitationTable SET CitationName = ? WHERE CitationID = ?",
                (new_name, citation_id))
            updated += 1

    report_file.write(
         "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
        f"Database updated: {'yes' if updated else 'no'}.\n\n"
        f"Citation Name values changed: {updated}.\n\n"
         "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
        )

    # Problem reports
    # Unresolved fields summary
    if unresolved_fields:
        report_file.write(
            "\n\n"
            "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
            "UNRESOLVED DATA FIELDS (Cannot be substituted in citation names)\n\n"
            )

        # Group by template and collect unique fields
        by_template = {}
        for unresolved in unresolved_fields.values():
            template_name = unresolved['template_name']
            if template_name not in by_template:
                by_template[template_name] = set()
            by_template[template_name].add(unresolved['field_name'])

        for template_name in sorted(by_template.keys()):
            field_names = sorted(by_template[template_name])
            field_list = ", ".join(f"[{name}]" for name in field_names)
            report_file.write(
                f"Source Template: {template_name} - {len(field_names)} unresolved field(s)\n"
                f"  {field_list}\n\n")
    else:
        report_file.write(
            "\n\n"
            "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
            "No unresolved data fields found.\n"
            "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
            )
    report_file.write(
        "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
    )

    return 0


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==


