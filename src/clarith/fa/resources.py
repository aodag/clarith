from fanstatic import Library, Resource
from js.tinymce import tinymce
from js.jquery import jquery

clarith_library = Library("clarith", "fanstatic_resources")
richtextfield = Resource(clarith_library, "js/richtextfield.js",
                         depends=[jquery, tinymce])
