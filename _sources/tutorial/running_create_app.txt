Creating the Application Skeleton
=====================================

Here is a session I used to create the initial skeleton. The command on the first
line below resulted in a question being asked, and I selected the default
answer.::

  ~/pyseqsee$ python3.2 farg/tools/pyseqsee_create_app.py numeric_bongard
  Using templates in  /home/amahabal/pyseqsee/data/pyseqsee_app_template
  New Destination:  farg/apps/numeric_bongard
  Enter Application Class (capitalized version of numeric_bongard) ['NumericBongard']:

Generated files
------------------

The command generated a bunch of files::

        farg/apps/numeric_bongard:
                batch_ui.py
                controller.py
                read_input_spec.py
                run_numeric_bongard.py
                stopping_conditions.py
                testing_input.txt
                workspace.py

        farg/apps/numeric_bongard/codelet_families:
                __init__.py

        farg/apps/numeric_bongard/gui:
                gui.py
                __init__.py
                workspace_view.py



