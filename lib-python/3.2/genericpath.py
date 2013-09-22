"""
Path operations common to more than one OS
Do not use directly.  The OS specific modules import the appropriate
functions from this module themselves.
"""
import os
import stat

from typing import (
    Any as Any_, List as List_, AnyStr as AnyStr_, Tuple as Tuple_
)

__all__ = ['commonprefix', 'exists', 'getatime', 'getctime', 'getmtime',
           'getsize', 'isdir', 'isfile']


# Does a path exist?
# This is false for dangling symbolic links on systems that support them.
def exists(path: AnyStr_) -> bool:
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        os.stat(path)
    except os.error:
        return False
    return True


# This follows symbolic links, so both islink() and isdir() can be true
# for the same path ono systems that support symlinks
def isfile(path: AnyStr_) -> bool:
    """Test whether a path is a regular file"""
    try:
        st = os.stat(path)
    except os.error:
        return False
    return stat.S_ISREG(st.st_mode)


# Is a path a directory?
# This follows symbolic links, so both islink() and isdir()
# can be true for the same path on systems that support symlinks
def isdir(s: AnyStr_) -> bool:
    """Return true if the pathname refers to an existing directory."""
    try:
        st = os.stat(s)
    except os.error:
        return False
    return stat.S_ISDIR(st.st_mode)


def getsize(filename: AnyStr_) -> int:
    """Return the size of a file, reported by os.stat()."""
    return os.stat(filename).st_size


def getmtime(filename: AnyStr_) -> float:
    """Return the last modification time of a file, reported by os.stat()."""
    return os.stat(filename).st_mtime


def getatime(filename: AnyStr_) -> float:
    """Return the last access time of a file, reported by os.stat()."""
    return os.stat(filename).st_atime


def getctime(filename: AnyStr_) -> float:
    """Return the metadata change time of a file, reported by os.stat()."""
    return os.stat(filename).st_ctime


# Return the longest prefix of all list elements.
def commonprefix(m: List_[AnyStr_]) -> Any_:
    "Given a list of pathnames, returns the longest common leading component"
    if not m: return ''
    s1 = min(m)
    s2 = max(m)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1


# Split a path in root and extension.
# The extension is everything starting at the last dot in the last
# pathname component; the root is everything before that.
# It is always true that root + ext == p.

# Generic implementation of splitext, to be parametrized with
# the separators
def _splitext(p: AnyStr_, sep: AnyStr_, altsep: AnyStr_,
              extsep: AnyStr_) -> Tuple_[AnyStr_, AnyStr_]:
    """Split the extension from a pathname.

    Extension is everything from the last dot to the end, ignoring
    leading dots.  Returns "(root, ext)"; ext may be empty."""
    # NOTE: This code must work for text and bytes strings.

    sepIndex = p.rfind(sep)
    if altsep:
        altsepIndex = p.rfind(altsep)
        sepIndex = max(sepIndex, altsepIndex)

    dotIndex = p.rfind(extsep)
    if dotIndex > sepIndex:
        # skip all leading dots
        filenameIndex = sepIndex + 1
        while filenameIndex < dotIndex:
            if p[filenameIndex:filenameIndex+1] != extsep:
                return p[:dotIndex], p[dotIndex:]
            filenameIndex += 1

    return p, p[:0]
