class Playlist(list):
	
  def __init__(self,media=None):
      super( Playlist, self ).__init__(media)
      self.current = 0

  def get_current(self):
      return self[self.current]

  def advance(self):
      self.current += 1
      if len(self) <= self.current :
          self.current=None
