#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Main ETL program.
#
# Author: Just van den Broecke
#
import optparse
from ConfigParser import ConfigParser
from setl.util import Util
from setl.chain import Chain

log = Util.get_log('main')

# The main program: build Chains of Components and let them run
class ETL:

    def __init__(self):
        usage = "usage: %prog -c <setl_config_file>"
        parser = optparse.OptionParser(usage)
        parser.add_option("-c", "--config", action="store", type="string", dest="config_file",
                          default="etl.cfg",
                          help="ETL config file")

        self.options, args = parser.parse_args()

        # Get config file path
        config_file = self.options.config_file
        log.info("config_file = %s" % config_file)
        self.configdict = ConfigParser()
        try:
            # parse config file
            self.configdict.read(config_file)
        except:
            log.warning("Found " + str(config_file) + " but cannot read it.")

    def run(self):
        # The main ETL processing
        log.info("START")

        # Get the ETL Chain pipeline config strings
        chains_str = self.configdict.get('etl', 'chains')
        if not chains_str:
            raise ValueError('ETL chain entry not defined in section [etl]')

        # Multiple Chains may be specified in the config
        chains_str_arr = chains_str.split(',')
        for chain_str in chains_str_arr:
            # Build single Chain of components and let it run
            chain = Chain(chain_str.strip(), self.configdict)
            chain.assemble()

            # Run the ETL for this Chain
            chain.run()

        log.info("ALL DONE")
