from core import client
import logging
from pluginbase import PluginBase
# Imports the main parts.

logger = logging.getLogger("highlightpy.entrypoint")
# Configures logging.

plugin_base = PluginBase(package='__main__.plugins')
plugin_source = plugin_base.make_plugin_source(
    searchpath=["./plugins"]
)
for plugin in plugin_source.list_plugins():
    plugin_source.load_plugin(plugin)
    logger.info(f"Loaded {plugin}.")
# Loads all of the plugins.

client.run()
# Starts the client.
