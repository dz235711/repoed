from enum import Enum

class VCS(str, Enum):
    GIT = "git"
    MERCURIAL = "mercurial"
    SUBVERSION = "subversion"
    BAZAAR = "bazaar"
    FOSSIL = "fossil"
    CVS = "cvs"