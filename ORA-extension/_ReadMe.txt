MH=MyHeritage.com
ANC=Ancestry.com

===========================================DIV50==

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
MANY ANCESTRY COLLECTIONS

lib.ANC-1person.ora
for collections involving 1 main person- birth, death,

lib.ANC-2person.ora
for collections involving 2 main person2- marriage, divorce

lib.ANC-1person.ora
There are many collections where this is ot working properly
The entered data includes Na,e birth date, and event date.
The event date should be simple and consistent, but it isn't.

e.g.
California Birth Index 1905-1995
id=5247
The Autotype
header:
<blank>
code:
[lib.ANC-1person]

The fields in the record-
Record ID	5247::21651620
URL	https://www.ancestry.com/discoveryui-content/view/21651620:5247
Name	Paige Janelleleigh Smtih
Birth Date	 4 July 1991
Gender	Female
Mother's Maiden Name	Beard
Birth County	Los Angeles
Source.Title	California Birth Index, 1905-1995
Source.Birthdate	 4 July 1991
Source.Birth County	Los Angeles
Source.Citation	Birthdate: 4 Jul 1991; Birth County: Los Angeles

the event date is auto typed by-
<{1:}
|[Baptism Date]
|[Arrival Date]
|[DeathDate]
|[Birth Year]
|[Birth Date]
|[Death Date]
|<abt [Estimated Birth Year:replace:abt ::l]>
>{TAB}

This uses Advanced list‑selector form. 
Seems to be optional and adds confusion.

the last option
<abt [Estimated Birth Year:replace:abt ::l]>
cleans up the date in some cases.

Make a list of fields in a separate file



ORA Help links

Text Template & Conditionals:
https://www.ora-extension.com/en/text-templates.htm
Conditionals:         < > & < |  |  >
Special References:   [?:varName]  [?:varName==TestVal]  etc.

AutoType:
https://www.ora-extension.com/en/auto-type.htm

Transforms:
https://www.ora-extension.com/en/text-templates.htm


ORA Troubleshooting

The Citation entry form must be tall enough so
that all fields are visible in window, otherwise the autotype
will fail by closing the window before the Research note is filled in.
Probably an RM issue with tabbing to a non visible field. 




