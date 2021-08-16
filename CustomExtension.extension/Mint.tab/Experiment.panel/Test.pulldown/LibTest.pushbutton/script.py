import Selection, FileUtilities, Warnings, QuestionableMath, FileUtilities, MEPUtilities
import sys
from pyrevit.coreutils import envvars
from pyrevit import DB, UI
print("\n".join(sys.path))

envvars.set_pyrevit_env_var('MINT_CONFIG', {'FAMILY_VIEW_ACTIVATED': False})
print('FAMILY_VIEW_ACTIVATED: ' + str(envvars.get_pyrevit_env_vars()['MINT_CONFIG']['FAMILY_VIEW_ACTIVATED']))