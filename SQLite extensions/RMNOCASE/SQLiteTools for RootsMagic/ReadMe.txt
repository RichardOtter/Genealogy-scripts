
direct download:
https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll

the link above is found in this context-
https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/


The SQLiteToolsforRootsMagic website has been around for many years and is run
by a trusted RM user. Many posts to public RootsMagic user forums mention use
of unifuzz64.dll from the SQLiteToolsforRootsMagic website.



MD5 hash values are used to confirm the identity and integrity of files.

    MD5 hash                            File size         File name
    06a1f485b0fae62caa80850a8c7fd7c2    256,406 bytes    unifuzz64.dll


History and Licensing


from- https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2019/01/unifuzz.c

**  legalese:   Don't look for a licence reference, there is none. Use this freely,
**              correct its bugs (there are certainly several waiting to destroy
**              your data), give it around, mail it to your representative/lover,
**              as you wish.  Credit DrH, Loic Dachary, Ioannis, Unicode groups
**              and any other contributor.


from- https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/

Unifuzz.c Source and compiling
unifuzz.c is readily compiled using the gcc compiler, mine came bundled in Dev-C++ Integrated Development Environment. I couldn’t figure out how to tell the IDE what I wanted to do but Jean-Christophe provided the command line for the gcc compiler at line 541 of his source code so I followed that. As the source is written, you want to extract to a folder the sqlite3.h and sqlite3ext.h files from the zip or tar file named sqlite-amalgamation-versionnumber on the SQLite Download Page under the heading Source Code. In a sub-folder below those .h files, place the unifuzz.c file. Then in the command line interface, issue:

pathtogcc\gcc -O2 -lm -shared unifuzz.c -o unifuzz64.dll
The DLL file will be produced in the same folder as the unifuzz.c file.
