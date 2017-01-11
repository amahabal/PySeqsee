How to create a new application
================================

I assume here that you have downloaded and installed PySeqsee and are in the root directory (
that is, you see the subdirectory 'farg' here). Follow these instructions to
create a project named bongard::

  farg create bongard

This will prompt you for an application name, and suggest the default 'Bongard'.
Press Enter to accept this. This will create a subdirectory within apps called
'bongard'.

Generated files
-----------------

The command above generates the following files::

        farg/apps/bongard:
                batch_ui.py
                controller.py
                read_input_spec.py
                run_numeric_bongard.py
                stopping_conditions.py
                testing_input.txt
                workspace.py

        farg/apps/bongard/codelet_families:
                __init__.py

        farg/apps/bongard/gui:
                gui.py
                __init__.py
                workspace_view.py

These files and the customization they require will be described in the coming sections.

Running the new app
------------------------

The new Bongard app does nothing useful yet. After all, it
knows of no codelets, its slipnet has no nodes, or any of the other wholesome
goodness you will add later. However, you can still take it for a spin with ::

  farg run bongard


You may click on the 'view' on the top left to look at different aspects of the app (such as the
coderack and the stream of thought, but all of these are of course currently empty.

