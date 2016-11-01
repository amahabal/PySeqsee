How to create a new application
================================

I assume here that you have downloaded PySeqsee and are in the root directory (
that is, you see the subdirectory 'farg' here). Follow these instructions to
create a project named Cat::

  /usr/bin/python3 -m farg.tools.pyseqsee_create_app cat

This will prompt you for an application name, and suggest the default 'Cat'.
Press Enter to accept this. This will create a subdirectory within apps called
'cat'. The directory will contain, amongst other things, the file 'run_cat.py'.
You can launch the new app like this::

  /usr/bin/python3 -m farg.apps.cat.run_cat

This should launch the app. It will not do anything useful yet. After all, it
knows of no codelets, its slipnet has no nodes, or any of the other wholesome
goodness you will add later. However, you can still click on the 'view' on the
top left to look at, say, the workspace and the coderack.
