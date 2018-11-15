from sql_gen.queries.queries import Keynames,EntityDefinition,ProcessDescriptor
from sql_gen import app


initial_context={'_keynames':Keynames(),
                  '_ed'      :EntityDefinition(),
                  '_pd'      :ProcessDescriptor(),
                  '_addb'    :app.ad_queryrunner
                 }
