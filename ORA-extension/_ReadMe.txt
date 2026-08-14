MH=MyHeritage.com
ANC=Ancestry.com


===========================================DIV50==
DNA Match Table entry

Purpose:
Extract data from an Ancestry DNA match page and enter it into the RootsMagic
DNA match edit window. This window has fixed fields that hold minimal information
but also includes a note field that can hold any text. Most data is entered into
the note filed in a parsable way: key=value.
For single line values,
key=--=value
For multi line values (or when value should start at col 0)
key=----=
value text 1
value text N
=----=

To set this up in the ORA options,
Create an AutoType position 1 using file:
DNA match ANC -AT#1.ora
or
DNA match MY -AT#1.ora

Create an AutoType position 2 using file:
DNA match ANC -AT#2.ora
or
DNA match MY -AT#2.ora

------
no code sharing

===========================================DIV50==
FindaGrave Citation Entry

Purpose:
Extract data from a Find a grave memorial page and enter it into a
RootsMagic citation entry window.
Assumes FG source exists and uses a specific template.

To set this up in the ORA options, need to create a Text Template using
the file "FindaGrave -TT#1 .ora". The file gives the heading name and the code.
Then an create an AutoType position 1 using file:
FindaGrave -AT#1.ora
Then an create an AutoType position 2 using file:
FindaGrave -AT#2.ora

------
Code shared through the Text Template with a public name
Shared because there is a new and update version that share most code.

===========================================DIV50==
Census Summary Fact Entry

Purpose:
Create a Census Fact in summary form. No citation created.
Needs to be shared with appropriate members, and Note edited 
to indicate missing people etc.
the keyword is changed to _SUMMARY-IMG when a census image 
is attached to the fact.

the Auto type simply calls the template library member with a parameter-
[lib.ANC-Census-Summary:YYYY]

------
Code shared through the Template library
All calls to the lib are the same, except for the YYYY parameter.

===========================================DIV50==
Template Library

lib.ANC-Census-Summary -FACT.ora
lib.ANC-1person.ora
lib.ANC-2person.ora

===========================================DIV50==







ORA Help links

Transforms:
https://www.ora-extension.com/en/text-templates.htm


ORA Troubleshooting

The Citation entry form must be tall enough so
that all fields are visible in window, otherwise the autotype
will fail by closing the window before the Research note is filled in.
Probably an RM issue with tabbing to a non visible field. 
