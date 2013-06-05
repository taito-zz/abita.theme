PROFILE_ID = 'profile-abita.theme:default'


def reimport_viewlets(setup):
    """Reimport viewlets"""
    setup.runImportStepFromProfile(PROFILE_ID, 'viewlets', run_dependencies=False, purge_old=False)


def reimport_typeinfo(setup):
    """Update typeinfo"""
    setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo', run_dependencies=False, purge_old=False)
