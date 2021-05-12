from termcolor import colored


class Contributor(object):
    def __init__(self, **kwargs):
        self.username = kwargs.get("username", None)
        self.validatedClipsBeginning = kwargs.get("validatedClipsBeginning", 0)
        self.recordedClipsBeginning = kwargs.get("recordedClipsBeginning", 0)
        self.clientHash = kwargs.get("clientHash", None)
        self.currentRecordedClips = None
        self.currentValidatedClips = None
        self.validatedClipsDelta = None
        self.recordedClipsDelta = None
        self.competitionScore = None

    def populateDeltas(self) -> None:
        try:
            self.validatedClipsDelta = self.currentValidatedClips - self.validatedClipsBeginning
        except TypeError:
            print(colored(
                f"{self.username} validatedClipsDelta threw error, so setting to 0", "red"))
            self.validatedClipsDelta = 0
        try:
            self.recordedClipsDelta = self.currentRecordedClips - self.recordedClipsBeginning
        except TypeError:
            print(colored(f"{self.username} recordedClipsDelta threw error, so setting to 0", "red"))
            self.recordedClipsDelta = 0

    def populateScore(self) -> None:
        self.competitionScore = (
            0.5 * self.validatedClipsDelta) + self.recordedClipsDelta

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)
