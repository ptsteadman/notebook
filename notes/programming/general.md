# General

There's always a tension between DRY (not defining a schema in multiple places)
and avoiding tight coupling.  Different parts of your application have different
requirements, and if a schema or object is only defined in one place, all other
parts of the application are tightly coupled to that one place.
