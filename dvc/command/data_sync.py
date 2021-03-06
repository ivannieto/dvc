from __future__ import unicode_literals

import argparse

import dvc.logger as logger
from dvc.command.base import CmdBase


class CmdDataBase(CmdBase):
    UP_TO_DATE_MSG = "Everything is up to date."

    def do_run(self, target):
        pass

    def run(self):
        if not self.args.targets:
            return self.do_run()

        ret = 0
        for target in self.args.targets:
            if self.do_run(target):
                ret = 1
        return ret

    @classmethod
    def check_up_to_date(cls, processed_files_count):
        if processed_files_count == 0:
            logger.info(cls.UP_TO_DATE_MSG)


class CmdDataPull(CmdDataBase):
    def do_run(self, target=None):
        try:
            processed_files_count = self.repo.pull(
                target=target,
                jobs=self.args.jobs,
                remote=self.args.remote,
                show_checksums=self.args.show_checksums,
                all_branches=self.args.all_branches,
                all_tags=self.args.all_tags,
                with_deps=self.args.with_deps,
                force=self.args.force,
                recursive=self.args.recursive,
            )
        except Exception:
            logger.error("failed to pull data from the cloud")
            return 1
        self.check_up_to_date(processed_files_count)
        return 0


class CmdDataPush(CmdDataBase):
    def do_run(self, target=None):
        try:
            processed_files_count = self.repo.push(
                target=target,
                jobs=self.args.jobs,
                remote=self.args.remote,
                show_checksums=self.args.show_checksums,
                all_branches=self.args.all_branches,
                all_tags=self.args.all_tags,
                with_deps=self.args.with_deps,
                recursive=self.args.recursive,
            )
        except Exception:
            logger.error("failed to push data to the cloud")
            return 1
        self.check_up_to_date(processed_files_count)
        return 0


class CmdDataFetch(CmdDataBase):
    def do_run(self, target=None):
        try:
            processed_files_count = self.repo.fetch(
                target=target,
                jobs=self.args.jobs,
                remote=self.args.remote,
                show_checksums=self.args.show_checksums,
                all_branches=self.args.all_branches,
                all_tags=self.args.all_tags,
                with_deps=self.args.with_deps,
                recursive=self.args.recursive,
            )
        except Exception:
            logger.error("failed to fetch data from the cloud")
            return 1
        self.check_up_to_date(processed_files_count)
        return 0


def shared_parent_parser():
    from dvc.cli import get_parent_parser

    # Parent parser used in pull/push/status
    shared_parent_parser = argparse.ArgumentParser(
        add_help=False, parents=[get_parent_parser()]
    )
    shared_parent_parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=None,
        help="Number of jobs to run simultaneously.",
    )
    shared_parent_parser.add_argument(
        "--show-checksums",
        action="store_true",
        default=False,
        help="Show checksums instead of file names.",
    )
    shared_parent_parser.add_argument(
        "targets", nargs="*", default=None, help="DVC files."
    )

    return shared_parent_parser


def add_parser(subparsers, _parent_parser):
    from dvc.command.status import CmdDataStatus

    # Pull
    PULL_HELP = (
        "Pull data files from the cloud.\n"
        "documentation: https://man.dvc.org/pull"
    )
    pull_parser = subparsers.add_parser(
        "pull",
        parents=[shared_parent_parser()],
        description=PULL_HELP,
        help=PULL_HELP,
    )
    pull_parser.add_argument(
        "-r", "--remote", help="Remote repository to pull from."
    )
    pull_parser.add_argument(
        "-a",
        "--all-branches",
        action="store_true",
        default=False,
        help="Fetch cache for all branches.",
    )
    pull_parser.add_argument(
        "-T",
        "--all-tags",
        action="store_true",
        default=False,
        help="Fetch cache for all tags.",
    )
    pull_parser.add_argument(
        "-d",
        "--with-deps",
        action="store_true",
        default=False,
        help="Fetch cache for all dependencies of the specified target.",
    )
    pull_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        default=False,
        help="Do not prompt when removing working directory files.",
    )
    pull_parser.add_argument(
        "-R",
        "--recursive",
        action="store_true",
        default=False,
        help="Pull cache for subdirectories of the specified directory.",
    )
    pull_parser.set_defaults(func=CmdDataPull)

    # Push
    PUSH_HELP = (
        "Push data files to the cloud.\n"
        "documentation: https://man.dvc.org/push"
    )
    push_parser = subparsers.add_parser(
        "push",
        parents=[shared_parent_parser()],
        description=PUSH_HELP,
        help=PUSH_HELP,
    )
    push_parser.add_argument(
        "-r", "--remote", help="Remote repository to push to."
    )
    push_parser.add_argument(
        "-a",
        "--all-branches",
        action="store_true",
        default=False,
        help="Push cache for all branches.",
    )
    push_parser.add_argument(
        "-T",
        "--all-tags",
        action="store_true",
        default=False,
        help="Push cache for all tags.",
    )
    push_parser.add_argument(
        "-d",
        "--with-deps",
        action="store_true",
        default=False,
        help="Push cache for all dependencies of the specified target.",
    )
    push_parser.add_argument(
        "-R",
        "--recursive",
        action="store_true",
        default=False,
        help="Push cache from subdirectories of specified directory.",
    )
    push_parser.set_defaults(func=CmdDataPush)

    # Fetch
    FETCH_HELP = (
        "Fetch data files from the cloud.\n"
        "documentation: https://man.dvc.org/fetch"
    )
    fetch_parser = subparsers.add_parser(
        "fetch",
        parents=[shared_parent_parser()],
        description=FETCH_HELP,
        help=FETCH_HELP,
    )
    fetch_parser.add_argument(
        "-r", "--remote", help="Remote repository to fetch from."
    )
    fetch_parser.add_argument(
        "-a",
        "--all-branches",
        action="store_true",
        default=False,
        help="Fetch cache for all branches.",
    )
    fetch_parser.add_argument(
        "-T",
        "--all-tags",
        action="store_true",
        default=False,
        help="Fetch cache for all tags.",
    )
    fetch_parser.add_argument(
        "-d",
        "--with-deps",
        action="store_true",
        default=False,
        help="Fetch cache for all dependencies of the " "specified target.",
    )
    fetch_parser.add_argument(
        "-R",
        "--recursive",
        action="store_true",
        default=False,
        help="Fetch cache for subdirectories of specified directory.",
    )
    fetch_parser.set_defaults(func=CmdDataFetch)

    # Status
    STATUS_HELP = (
        "Show the repo status.\ndocumentation: https://man.dvc.org/status"
    )
    status_parser = subparsers.add_parser(
        "status",
        parents=[shared_parent_parser()],
        description=STATUS_HELP,
        help=STATUS_HELP,
        conflict_handler="resolve",
    )
    status_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help=(
            "Suppresses all output."
            " Exit with 0 if pipeline is up to date, otherwise 1."
        ),
    )
    status_parser.add_argument(
        "-c",
        "--cloud",
        action="store_true",
        default=False,
        help="Show status of a local cache compared to a remote repository.",
    )
    status_parser.add_argument(
        "-r", "--remote", help="Remote repository to compare local cache to."
    )
    status_parser.add_argument(
        "-a",
        "--all-branches",
        action="store_true",
        default=False,
        help="Show status of a local cache compared to a remote repository "
        "for all branches.",
    )
    status_parser.add_argument(
        "-T",
        "--all-tags",
        action="store_true",
        default=False,
        help="Show status of a local cache compared to a remote repository "
        "for all tags.",
    )
    status_parser.add_argument(
        "-d",
        "--with-deps",
        action="store_true",
        default=False,
        help="Show status for all dependencies of the specified target.",
    )
    status_parser.set_defaults(func=CmdDataStatus)
