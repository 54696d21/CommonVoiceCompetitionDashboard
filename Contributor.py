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
        # print(f'{self.username=}')
        # print(f'{self.currentValidatedClips=}')
        # print(f'{self.validatedClipsBeginning=}')
        # print(f'{self.currentRecordedClips=}')
        # print(f'{self.recordedClipsBeginning=}')
        # self.validatedClipsDelta = self.currentValidatedClips - self.validatedClipsBeginning
        # self.recordedClipsDelta = self.currentRecordedClips - self.recordedClipsBeginning
        try:
            self.validatedClipsDelta = self.currentValidatedClips - self.validatedClipsBeginning
        except TypeError:
            self.validatedClipsDelta = 0
        try:
            self.recordedClipsDelta = self.currentRecordedClips - self.recordedClipsBeginning
        except TypeError:
            self.recordedClipsDelta = 0
        

    def populateScore(self) -> None:
        self.competitionScore = (
            0.5 * self.validatedClipsDelta) + self.recordedClipsDelta

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)
