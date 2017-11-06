# -------------------------------------------------------------------------
#                     The CodeChecker Infrastructure
#   This file is distributed under the University of Illinois Open Source
#   License. See LICENSE.TXT for details.
# -------------------------------------------------------------------------

import errno
import subprocess
import tempfile

from libcodechecker.logger import LoggerFactory

LOG = LoggerFactory.get_new_logger('HOST CHECK')


def check_clang(compiler_bin, env):
    """
    Simple check if clang is available.
    """
    clang_version_cmd = [compiler_bin, '--version']
    LOG.debug_analyzer(' '.join(clang_version_cmd))
    try:
        res = subprocess.call(clang_version_cmd,
                              env=env,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        if not res:
            return True

        LOG.debug_analyzer('Failed to run: "' + ' '.join(clang_version_cmd) +
                           '"')
        return False

    except OSError as oerr:
        if oerr.errno == errno.ENOENT:
            LOG.error(oerr)
            LOG.error('Failed to run: "' + ' '.join(clang_version_cmd) + '"')
            return False


def has_analyzer_feature(clang_bin, feature):
    with tempfile.NamedTemporaryFile() as inputFile:
        inputFile.write("void foo(){}")
        inputFile.flush()
        cmd = [clang_bin, "-x", "c", "--analyze",
               "-Xclang", feature, inputFile.name, "-o", "-"]
        LOG.debug('run: "' + ' '.join(cmd) + '"')
        try:
            proc = subprocess.Popen(cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    )
            out, err = proc.communicate()

            LOG.debug("stdout:\n" + out)
            LOG.debug("stderr:\n" + err)

            return proc.returncode == 0
        except OSError:
            LOG.error('Failed to run: "' + ' '.join(cmd) + '"')
            raise
