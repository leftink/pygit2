# Copyright 2010-2020 The pygit2 contributors
#
# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2,
# as published by the Free Software Foundation.
#
# In addition to the permissions in the GNU General Public License,
# the authors give you unlimited permission to link the compiled
# version of this file into combinations with other programs,
# and to distribute those combinations without any restriction
# coming from the use of this file.  (The General Public License
# restrictions do apply in other respects; for example, they cover
# modification of the file, and distribution when not linked into
# a combined executable.)
#
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

import pytest

import pygit2
from . import utils


BLOB_OLD_SHA = 'a520c24d85fbfc815d385957eed41406ca5a860b'
BLOB_NEW_SHA = '3b18e512dba79e4c8300dd08aeb37f8e728b8dad'
BLOB_OLD_CONTENT = b"""hello world
hola mundo
bonjour le monde
"""
BLOB_NEW_CONTENT = b'foo bar\n'

BLOB_OLD_PATH = 'a/file'
BLOB_NEW_PATH = 'b/file'

BLOB_PATCH2 = """diff --git a/a/file b/b/file
index a520c24..3b18e51 100644
--- a/a/file
+++ b/b/file
@@ -1,3 +1 @@
 hello world
-hola mundo
-bonjour le monde
"""

BLOB_PATCH = """diff --git a/a/file b/b/file
index a520c24..d675fa4 100644
--- a/a/file
+++ b/b/file
@@ -1,3 +1 @@
-hello world
-hola mundo
-bonjour le monde
+foo bar
"""

BLOB_PATCH_ADDED = """diff --git a/a/file b/b/file
new file mode 100644
index 0000000..d675fa4
--- /dev/null
+++ b/b/file
@@ -0,0 +1 @@
+foo bar
"""

BLOB_PATCH_DELETED = """diff --git a/a/file b/b/file
deleted file mode 100644
index a520c24..0000000
--- a/a/file
+++ /dev/null
@@ -1,3 +0,0 @@
-hello world
-hola mundo
-bonjour le monde
"""


class PatchTest(utils.RepoTestCase):

    def test_patch_create_from_buffers(self):
        patch = pygit2.Patch.create_from(
            BLOB_OLD_CONTENT,
            BLOB_NEW_CONTENT,
            old_as_path=BLOB_OLD_PATH,
            new_as_path=BLOB_NEW_PATH,
        )

        assert patch.text == BLOB_PATCH

    def test_patch_create_from_blobs(self):
        old_blob = self.repo[BLOB_OLD_SHA]
        new_blob = self.repo[BLOB_NEW_SHA]

        patch = pygit2.Patch.create_from(
            old_blob,
            new_blob,
            old_as_path=BLOB_OLD_PATH,
            new_as_path=BLOB_NEW_PATH,
        )

        assert patch.text == BLOB_PATCH2

    def test_patch_create_from_blob_buffer(self):
        old_blob = self.repo[BLOB_OLD_SHA]
        patch = pygit2.Patch.create_from(
            old_blob,
            BLOB_NEW_CONTENT,
            old_as_path=BLOB_OLD_PATH,
            new_as_path=BLOB_NEW_PATH,
        )

        assert patch.text == BLOB_PATCH

    def test_patch_create_from_blob_buffer_add(self):
        patch = pygit2.Patch.create_from(
            None,
            BLOB_NEW_CONTENT,
            old_as_path=BLOB_OLD_PATH,
            new_as_path=BLOB_NEW_PATH,
        )

        assert patch.text == BLOB_PATCH_ADDED

    def test_patch_create_from_blob_buffer_delete(self):
        old_blob = self.repo[BLOB_OLD_SHA]

        patch = pygit2.Patch.create_from(
            old_blob,
            None,
            old_as_path=BLOB_OLD_PATH,
            new_as_path=BLOB_NEW_PATH,
        )

        assert patch.text == BLOB_PATCH_DELETED

    def test_patch_create_from_bad_old_type_arg(self):
        with pytest.raises(TypeError):
            pygit2.Patch.create_from(self.repo, BLOB_NEW_CONTENT)

    def test_patch_create_from_bad_new_type_arg(self):
        with pytest.raises(TypeError):
            pygit2.Patch.create_from(None, self.repo)

    def test_context_lines(self):
        old_blob = self.repo[BLOB_OLD_SHA]
        new_blob = self.repo[BLOB_NEW_SHA]

        patch = pygit2.Patch.create_from(
            old_blob,
            new_blob,
            old_as_path=BLOB_OLD_PATH,
            new_as_path=BLOB_NEW_PATH,
        )

        context_count = len(
            [line for line in patch.text.splitlines() if line.startswith(" ")]
        )

        assert context_count != 0

    def test_no_context_lines(self):
        old_blob = self.repo[BLOB_OLD_SHA]
        new_blob = self.repo[BLOB_NEW_SHA]

        patch = pygit2.Patch.create_from(
            old_blob,
            new_blob,
            old_as_path=BLOB_OLD_PATH,
            new_as_path=BLOB_NEW_PATH,
            context_lines=0,
        )

        context_count = len(
            [line for line in patch.text.splitlines() if line.startswith(" ")]
        )

        assert context_count == 0

    def test_patch_create_blob_blobs(self):
        old_blob = self.repo[self.repo.create_blob(BLOB_OLD_CONTENT)]
        new_blob = self.repo[self.repo.create_blob(BLOB_NEW_CONTENT)]

        patch = pygit2.Patch.create_from(
            old_blob,
            new_blob,
            old_as_path=BLOB_OLD_PATH,
            new_as_path=BLOB_NEW_PATH,
        )

        assert patch.text == BLOB_PATCH

    def test_patch_create_blob_buffer(self):
        blob = self.repo[self.repo.create_blob(BLOB_OLD_CONTENT)]
        patch = pygit2.Patch.create_from(
            blob,
            BLOB_NEW_CONTENT,
            old_as_path=BLOB_OLD_PATH,
            new_as_path=BLOB_NEW_PATH,
        )

        assert patch.text == BLOB_PATCH

    def test_patch_create_blob_delete(self):
        blob = self.repo[self.repo.create_blob(BLOB_OLD_CONTENT)]
        patch = pygit2.Patch.create_from(
            blob,
            None,
            old_as_path=BLOB_OLD_PATH,
            new_as_path=BLOB_NEW_PATH,
        )

        assert patch.text == BLOB_PATCH_DELETED

    def test_patch_create_blob_add(self):
        blob = self.repo[self.repo.create_blob(BLOB_NEW_CONTENT)]
        patch = pygit2.Patch.create_from(
            None,
            blob,
            old_as_path=BLOB_OLD_PATH,
            new_as_path=BLOB_NEW_PATH,
        )

        assert patch.text == BLOB_PATCH_ADDED

    def test_patch_delete_blob(self):
        blob = self.repo[BLOB_OLD_SHA]
        patch = pygit2.Patch.create_from(
            blob,
            None,
            old_as_path=BLOB_OLD_PATH,
            new_as_path=BLOB_NEW_PATH,
        )

        # Make sure that even after deleting the blob the patch still has the
        # necessary references to generate its patch
        del blob
        assert patch.text == BLOB_PATCH_DELETED

    def test_patch_multi_blob(self):
        blob = self.repo[BLOB_OLD_SHA]
        patch = pygit2.Patch.create_from(
            blob,
            None
        )
        patch_text = patch.text

        blob = self.repo[BLOB_OLD_SHA]
        patch2 = pygit2.Patch.create_from(
            blob,
            None
        )
        patch_text2 = patch.text

        assert patch_text == patch_text2
        assert patch_text == patch.text
        assert patch_text2 == patch2.text
        assert patch.text == patch2.text


expected_diff = b"""diff --git a/iso-8859-1.txt b/iso-8859-1.txt
index e84e339..201e0c9 100644
--- a/iso-8859-1.txt
+++ b/iso-8859-1.txt
@@ -1 +1,2 @@
 Kristian H\xf8gsberg
+foo
"""

def test_patch_from_non_utf8():
    # blobs encoded in ISO-8859-1
    old_content = b'Kristian H\xf8gsberg\n'
    new_content = old_content + b'foo\n'
    patch = pygit2.Patch.create_from(
        old_content,
        new_content,
        old_as_path='iso-8859-1.txt',
        new_as_path='iso-8859-1.txt',
    )

    assert patch.data == expected_diff
    assert patch.text == expected_diff.decode('utf-8', errors='replace')

    # `patch.text` corrupted the ISO-8859-1 content as it forced UTF-8
    # decoding, so assert that we cannot get the original content back:
    assert patch.text.encode('utf-8') != expected_diff

def test_patch_create_from_blobs(encodingrepo):
    patch = pygit2.Patch.create_from(
        encodingrepo['e84e339ac7fcc823106efa65a6972d7a20016c85'],
        encodingrepo['201e0c908e3d9f526659df3e556c3d06384ef0df'],
        old_as_path='iso-8859-1.txt',
        new_as_path='iso-8859-1.txt',
    )

    assert patch.data == expected_diff
    assert patch.text == expected_diff.decode('utf-8', errors='replace')

    # `patch.text` corrupted the ISO-8859-1 content as it forced UTF-8
    # decoding, so assert that we cannot get the original content back:
    assert patch.text.encode('utf-8') != expected_diff
