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

import bandit.bandit_baseline as baseline

import fixtures
import os
import subprocess
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

    def test_bandit_baseline(self):
        repo_directory = self.useFixture(fixtures.TempDir()).path

        files = [('benign_one.py', benign_contents),
                 ('benign_two.py', benign_contents),
                 ('malicious.py', malicious_contents)]

        for fname, contents in files:
            with open(os.path.join(repo_directory, fname), 'wt') as output:
                output.write(contents)

        # init git repo, change directory to it
        git_repo = git.Repo.init(repo_directory, mkdir=False)
        os.chdir(repo_directory)

        # create three commits, first has only file_a, second adds file_b,
        # third adds file-c
        git_repo.index.add(['benign_one.py'])
        git_repo.index.commit('Commit A')

        git_repo.index.add(['benign_one.py', 'malicious.py'])
        git_repo.index.commit('Commit B')

        git_repo.index.add(['benign_one.py', 'malicious.py', 'benign_two.py'])
        git_repo.index.commit('Commit C')

        commits = list(git_repo.iter_commits())

        # we expect this to return 1 because the malicious contents file was
        # added, which means there will be baseline findings
        git_repo.head.reset(commit=commits[1], working_tree=True)
        self.assertEqual(subprocess.call(['bandit-baseline', '-r', '.']), 1)

        # we expect this to return 0 because the benign contents file was added
        # which means no baseline findings
        git_repo.head.reset(commit=commits[0], working_tree=True)
        self.assertEqual(subprocess.call(['bandit-baseline', '-r', '.']), 0)

        subprocess.call(['rm', '-rf', repo_directory])
