""" Report Class Module """

import sys
import logging
from typing import Any
from dataclasses import dataclass, field
from yaml import safe_load
from router.data_router import handler


@dataclass
class Report:
    """ Report Module with the following attributes:
        - Name: Report's Name
        - Config:
    """
    name: str
    config: dict = field(init=False)
    data: Any = field(init=False)
    data_sources: dict = field(init=False)
    report_path: str
    template_path: str
    template_name: str = field(init=False)
    to_pdf: bool
    to_html: bool


    def load_config(self, config=None):
        """
        :param config-> optional configuration passed in on load.
            Will be used to give the option to pass in config
            from STDIN

        Attempts to load a configuration for the report from
        STDIN, then checks for preloaded report_config, finally
        looks for a yaml configuration.

        """
        if config:
            self.config = config
        else:
            self.config_from_file()

        self.template_name = self.config.get("template")
        self.data_sources = self.config.get("data")


    def config_from_file(self):
        """Load Report Config from file"""

        config_path = f"{self.report_path}/{self.name}.yml"
        try:
            with open(config_path, "r", encoding="UTF-8") as file:
                config = safe_load(file).get("report")
        except FileNotFoundError as err:  # raise exception
            logging.fatal("No report configuration found, %s", err)
            sys.exit()
        else:
            self.config = config


    def load_data(self):
        """ Loads the data for the Report. Must be run after load_config """

        if not self.data_sources:
            logging.error("Data sources have not been loaded")
        self.data = handler(self.data_sources)
