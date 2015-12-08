# -*- coding:utf-8 -*-
#
# Copyright 2015 Hewlett-Packard Enterprise
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import subprocess
import tempfile
import testtools

import git


benign_contents = """
something_benign()
"""

malicious_contents = """
import os

os.system('do/something' + bad)
"""


class BanditBaselineToolTests(testtools.TestCase):

    def setUp(self):
        super(BanditBaselineToolTests, self).setUp()
        self.repo_directory = tempfile.mkdtemp()

        file_a = self.repo_directory + '/file_a.py'
        file_b = self.repo_directory + '/file_b.py'
        file_c = self.repo_directory + '/file_c.py'

        # create file_a, file_b, file_c -- file_a and file_c are benign, file_b
        # has Bandit findings

        with open(self.repo_directory + '/file_a.py', 'w') as f:
            f.write(benign_contents)

        with open(self.repo_directory + '/file_b.py', 'w') as f:
            f.write(malicious_contents)

        with open(self.repo_directory + '/file_c.py', 'w') as f:
            f.write(benign_contents)

        # init git repo, change directory to it
        self.git_repo = git.Repo.init(self.repo_directory, mkdir=False)
        os.chdir(self.repo_directory)

        # create three commits, first has only file_a, second adds file_b,
        # third adds file-c
        self.git_repo.index.add([file_a])
        self.git_repo.index.commit('Commit A')

        self.git_repo.index.add([file_a, file_b])
        self.git_repo.index.commit('Commit B')

        self.git_repo.index.add([file_a, file_b, file_c])
        self.git_repo.index.commit('Commit C')

        self.commits = list(self.git_repo.iter_commits())

    def test_bandit_baseline(self):
        # we expect this to return 1 because the malicious contents file was
        # added, which means there will be baseline findings
        self.git_repo.head.reset(commit=self.commits[1], working_tree=True)
        self.assertEqual(subprocess.call(['bandit-baseline', '-r', '.']), 1)

        # we expect this to return 0 because the benign contents file was added
        # which means no baseline findings
        self.git_repo.head.reset(commit=self.commits[0], working_tree=True)
        self.assertEqual(subprocess.call(['bandit-baseline', '-r', '.']), 0)

    def tearDown(self):
        super(BanditBaselineToolTests, self).tearDown()
        subprocess.call(['rm', '-rf', self.repo_directory])
