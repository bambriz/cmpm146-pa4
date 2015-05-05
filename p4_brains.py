#Bryan Erick Ambriz
import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None

  def handle_event(self, message, details):

    if self.state is 'idle':

      if message == 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state == 'curious':

      if message == 'timer':
        # chase down that slug who bumped into us
        if self.target:
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite

class SlugBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None
    self.have_resource = False
    self.aware = True
    self.counter = 0

  def handle_event(self, message, details):
    # TODO: IMPLEMENT THIS METHOD
    #  (Use helper methods and classes to keep your code organized where
    #  approprioate.)
    ###Code starts here
    #
    #
    #
    self.target = None
    #
    #
    #order
    # When the user right-clicks a map location when some units selected, an event like this will be dispatched.
    if message == 'order':
      try:
        x, y = details
        self.body.go_to(details)
        pass
      except ValueError:
        if details == 'i':
          self.state = 'idle'
          self.body.stop()
          pass
        elif details == 'a':
          self.state = 'attack'
          pass
        elif details == 'h':
          self.state = 'harvest'
          pass
        elif details == 'b':
          self.state = 'build'
          pass
        elif details == 'd':
          self.body.amount = .4
          pass
#
#When the user presses a, the selected slug units should enter an attack mode.
#
#In this mode, the slug should periodically (every one or two seconds)
# find the nearest Mantis unit (using find_nearest) and begin following it (using follow).
#Upon colliding with a mantis in attack mode,
# the mantis amount should be decremented by 0.05 units per collision event.
#The logic of this command should allow a single slug to seek and destroy several mantises
# (not getting stuck after the first one).

#
#
#
    if self.state == 'attack':
      try:
        self.target = self.body.find_nearest("Mantis")
        self.body.follow(self.target)
        if message == 'collide' and details['who'] == self.target:
          self.target.amount -= .05
          self.body.set_alarm(2)
      except ValueError:
        self.body.stop()
        self.state = 'idle'
#
#When the user presses h, the selected slug units should enter a harvest mode.
#In order to correctly implement harvesting behavior, you will need to store
#  some extra state in the brain as to whether the slug carries some resource or not.
# (Define an extra field in the SlugBrain constructor. Consider a line like self.have_resource = False.)
#If the slug is holding a resource, it should periodically
# find and approach the nearest Nest. If the slug is not holding
#  a resource, it should periodically find and approach the nearest Resource object.
#When colliding with a Resource object while not holding a resource,
#  decrement the amount of the Resource object by 0.25 (and set your have_resource flag accordingly)
#When colliding with a Nest while holding a resource, simply reset the
#  resource holding flag. (Leave the amount of the Nest untouched so
# that it is clear when it is being changed by a slug in the build mode.)
#Several slugs should be able to autonomously mine out several Resource
#  objects near a given nest without user intervention. (The Resource
# objects are destroyed when their amount drops below zero.)

#
    if self.state == 'harvest':
      if self.have_resource == False:
        try:
          self.target = self.body.find_nearest("Resource")
          self.body.go_to(self.target)
          if message == 'collide' and details['who'] == self.target:
            self.target.amount -= .25
            self.have_resource = True
        except ValueError:
          self.body.stop()
          self.state = 'idle'
      else:
        self.target = self.body.find_nearest("Nest")
        self.body.go_to(self.target)
        if message == 'collide' and details['who'] == self.target:
          self.have_resource = False
      self.body.set_alarm(2)

#
#When the user presses b, the selected slug units should enter a build mode.
#In this mode, the slug should periodically find the nearest
#  nest and approach it (using go_to).
#When colliding with a Nest in build mode,
#  the amount of the nest should be incremented by 0.01 per collision event.
#It is not expected that a slug in build mode will approach
# the Nest with least amount or move on to another Nest once the nearest
# has been fully built. Manipulating the builders focus is the players
#  responsibility for this particular game.

#

    if self.state == 'build':
      self.target = self.body.find_nearest("Nest")
      self.body.go_to(self.target)
      if message == 'collide' and details['who'] == self.target and self.target.amount < 1:
        self.target.amount += .01
      if self.target.amount == 1:
        self.body.stop()
        self.state = 'idle'
      self.body.set_alarm(2)
#
#Whenever slug has low health (amount less than 0.5), the slug should
# immediately start moving to (using either go_to or follow) the nearest Nest.
#  No user intervention should be required to enter flee mode.
#When colliding with a Nest in Flee mode, the slugs health (amount)
#  should be restored (whether it goes to full in one step or several
#  small steps is up to the student to decide).
#
#
    if self.body.amount < .5:
      self.state = 'Flee'

    if self.state == 'Flee':
      self.target = self.body.find_nearest("Nest")
      self.body.go_to(self.target)
      if message == 'collide' and details['who'] == self.target and self.target.amount < 1:
        self.body.amount = 1
        self.target = None
        self.body.stop()
        self.state = 'idle'
      self.body.set_alarm(2)

    pass

world_specification = {
  'worldgen_seed': 13, # comment-out to randomize
  'nests': 2,
  'obstacles': 25,
  'resources': 5,
  'slugs': 5,
  'mantises': 5,
}

brain_classes = {
  'mantis': MantisBrain,
  'slug': SlugBrain,
}
