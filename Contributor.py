class Contributor(object):
    def __init__(self, **kwargs):
        self.username = kwargs.get("username", None)
        self.validatedClipsBeginning = kwargs.get(
            "validatedClipsBeginning", None)
        self.recordedClipsBeginning = kwargs.get(
            "recordedClipsBeginning", None)
        self.clientHash = kwargs.get("clientHash", None)
        self.currentRecordedClips = None
        self.currentValidatedClips = None
        self.validatedClipsDelta = None
        self.recordedClipsDelta = None
        self.competitionScore = None

    def populateDeltas(self) -> None:
        self.validatedClipsDelta = self.currentValidatedClips - self.validatedClipsBeginning
        self.recordedClipsDelta = self.currentRecordedClips - self.recordedClipsBeginning

    def populateScore(self) -> None:
        self.competitionScore = (
            0.5 * self.validatedClipsDelta) + self.recordedClipsDelta

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)
