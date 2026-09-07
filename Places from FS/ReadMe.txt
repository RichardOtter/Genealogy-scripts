Categories of place names

german
has a ~
has [] text for strict place value
has ?
has _skip in note

final auxplaetable should have
orig name  (fail safe)
returned fs name in english
retruned fs name in german
RJO modified name (has [] text for place holder ?)

parent id


Strategy
create the new AuxPlaceTable
Run the sql to populate it with the orig data in PlaceTable
update the FSPID from the Orig_Note
run sql to update the Uncertain column (if the orig name has a ~ or a ?)
Uncertain=_PROBABLY  if name has ~
         =_UNCLEAR   if name has ?
         =_REGION    if name has region
         =_VICINITY  if name has vicinity
--how about place holder text [IC] etc
run sql to update the Language column: en or de
run SQL to update NonFSPlace if currently has _SKIP


Wladzell
current time
FSPID=9835723
Jurisdiction / parent ID: 9286763 Parent: Steinfeld

Primary ID=3864248


https://api.familysearch.org/platform/places/3864248
gives all the descriptions.
