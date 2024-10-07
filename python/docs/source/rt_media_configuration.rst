.. 5GMS Application Provider documentation master file, created by
   sphinx-quickstart on Mon Oct  7 11:21:51 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

`rt_media_configuration` module
===============================

The `rt_media_configuration` module is responsible for providing a model that represents the data needed for both the interface at reference point M1 and some basic extra metadata that is to be distributed by the Application Provider via the interface at reference point M8.

The model can be built via the modules API classes and methods or can be imported from a JSON description or the existing configuration in the 5GMS Application Function.

The model can then be synchronised with the 5GMS Application Function (AF), at which point any changes between the model and the current 5GMS AF are pushed to the 5GMS AF and the M8 only metadata associated with that configuration is stored in the persistent DataStore. Upon retrieving the model from the 5GMS AF the persistent data is reloaded to fill in the metadata that is not part of the 5GMS AF provisioning.

After the model has been sychronised with the 5GMS AF this module will cause the M8 published files to be written out or updated. This will help the 5GMS Aware Application to keep its configuration synchronised with the current state of the 5GMS AF.

.. mermaid:: rt_media_configuration-classes.mmd

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. automodule:: rt_media_configuration
   :members:
   :undoc-members:
   :member-order: groupwise
   :show-inheritance:
