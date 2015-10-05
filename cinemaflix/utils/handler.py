import os
import subprocess


class ResourceNotFoundException(Exception):
    pass


class TorrentHandler(object):

    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.players = ['vlc', 'mpv', 'mplayer']

    def stream_with_peerflix(self, link, player, subtitle=None):
        if player not in self.players:
            raise ResourceNotFoundException('Player Not Found')
        if not self.is_installed('peerflix'):
            raise ResourceNotFoundException('Peerflix Not Found')
        command = "peerflix '{}' --{} --subtitles '{}' -f {} -d".format(
            link, player, subtitle, self.cache_path)
        print command
        subprocess.Popen(command, shell=True)

    def stream_with_webtorrent(self, link, player, subtitle=None):
        if player not in self.players:
            raise ResourceNotFoundException('Player Not Found')
        if not self.is_installed('peerflix'):
            raise ResourceNotFoundException('WebTorrent Not Found')
        command = "webtorrent '{}' --{} --subtitles '{}' -o {}".format(
            link, player, subtitle, self.cache_path)
        print command
        subprocess.Popen(command)

    def stream(self, handler, link, player, subtitle=None):
        if handler == "peerflix":
            self.stream_with_peerflix(link, player, subtitle)
        elif handler == "webtorrent":
            self.stream_with_webtorrent(link, player, subtitle)
        else:
            print "handler not supported"

    @staticmethod
    def is_installed(cmd):
        inst = lambda x: any(os.access(os.path.join(path, x), os.X_OK) for path
                             in os.environ["PATH"].split(os.pathsep))
        return inst(cmd)