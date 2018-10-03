from .client import client


class Cog:
    """A base cog for all other cogs."""
    @property
    def commands(self):
        """Gets the commands from a cog."""
        return client.get_cog_commands(self.name)

    @property
    def name(self):
        """Returns the cogs name."""
        return self.__class__.__name__
