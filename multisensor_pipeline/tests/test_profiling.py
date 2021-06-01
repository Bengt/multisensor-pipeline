import unittest
from random import randint
from time import sleep
from typing import List

from multisensor_pipeline.dataframe.dataframe import MSPDataFrame
from multisensor_pipeline.modules.base.profiling import MSPModuleStats


class ProfilingTest(unittest.TestCase):
    def test_frequency_stats(self):
        frequency = 10
        msp_stats = MSPModuleStats()
        frames: List = []
        for _ in range(20):
            frames.append(MSPDataFrame(topic="test", value=randint(0, 20)))

        for frame in frames:
            msp_stats.add_frame(frame, direction=MSPModuleStats.Direction.IN)
            sleep(1./frequency)

        stats = msp_stats.get_stats(direction=MSPModuleStats.Direction.IN)
        self.assertAlmostEqual(10, stats["test"]._cma, delta=1)
        self.assertAlmostEqual(10, stats["test"]._sma, delta=1)

    def test_frequency_stats_again(self):
        msp_stats = MSPModuleStats()
        frames = []
        # FIXME: does not work with higher frame rate because of sleep
        for _ in range(0, 50):
            frames.append(MSPDataFrame(topic="test", value=randint(0, 20)))

        for frame in frames:
            msp_stats.add_frame(
                frame=frame,
                direction=MSPModuleStats.Direction.IN,
            )
            sleep(1./10)

        stats = msp_stats.get_stats(direction=MSPModuleStats.Direction.IN)
        self.assertAlmostEqual(10, stats["test"]._cma, delta=1)
