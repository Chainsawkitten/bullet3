import functools
import inspect
import pybullet


class BulletClient(object):
  """A wrapper for pybullet to manage different clients."""

  def __init__(self, connection_mode=pybullet.DIRECT):
    """Create a simulation and connect to it."""
    self._client = pybullet.connect(connection_mode)
    self._shapes = {}

  def __del__(self):
    """Clean up connection if not already done."""
    try:
      pybullet.disconnect(physicsClientId=self._client)
    except pybullet.error:
      pass

  def __getattr__(self, name):
    """Inject the client id into Bullet functions."""
    attribute = getattr(pybullet, name)
    if inspect.isbuiltin(attribute):
      if name not in ["invertTransform", "multiplyTransforms",
                      "getMatrixFromQuaternion"]:  # A temporary hack for now.
        attribute = functools.partial(attribute, physicsClientId=self._client)
    return attribute

