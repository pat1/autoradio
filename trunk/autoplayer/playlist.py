class Playlist(list):
	
  def __init__(self,media=None):
    super( Playlist, self ).__init__(media)
    if len (self) == 0 :
      self.current = None
    else:
      self.current = 0
    
  def get_current(self):
    if self.current is not None: 
      return self[self.current]
    else:
      return None

  def advance(self):
    if self.current is not None: 
      self.current += 1
      if len(self) <= self.current :
        self.current=None

