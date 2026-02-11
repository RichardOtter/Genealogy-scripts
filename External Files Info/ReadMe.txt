External Files Info




#   EXTERNALFILESINFO_ADD_FAST
# most common task when the number of files is large and speed is desired

# do not Create Aux table if missing, just print error
# do not do any data compares
# go thru media list, list missing files and db entries with no info 
# find missing aux rows and add them with full fs data

#   EXTERNALFILESINFO_ADD
# done for first run

# Create AuxMultimediaTable if missing
# go thru media list, list missing files and db entries with no info 
# find missing aux rows and add them with full fs data
# do compare of db vs fs for existing aux media records, list mismatches

#   EXTERNALFILESINFO_COMPARE
# do not Create Aux table if missing, just print error
# go thru media list, list missing files and db entries with no info 
# do compare but do not add or update

#   EXTERNALFILESINFO_UPDATE
# do not Create Aux table if missing, just print error
# go thru list, ignore missing files and db entries with no info
# do compares db vs fs
# update aux rows if data for filesystem file has changed

