import os
from typing import Union, List, Tuple
from xml.dom import minicompat

import gym
import gym.spaces
from PIL import Image
import numpy as np

from env.miniwob.miniwob_interface.action import (
    MiniWoBPress,
    MiniWoBRelease,
    MiniWoBAction,
    MiniWoBCoordClick,
    MiniWoBType,
    MiniWoBElementClickId,
    MiniWoBElementClickXpath,
    MiniWoBElementClickOption,
)
from env.miniwob.miniwob_interface.environment import MiniWoBEnvironment

cur_path_dir = os.path.dirname(os.path.realpath(__file__))
miniwob_dir = os.path.join(cur_path_dir, "miniwob_interface", "html", "miniwob")


class MiniWoBEnv(MiniWoBEnvironment, gym.Env):
    """

    ### Observation Space

    The observation is a screen image (width x height x RGB) = (160 x 210 x 3)

    ### Action Space (action type, x coordinate, y coordinate)

    | type  | action type
    |-------|-------------------------------------------------------------
    | 0     | Mouse click and hold
    | 1     | Mouse release
    | 2     | Mouse click

    |   type  | x coordinate
    |---------|-------------------------------------------------------------
    | 0 ~ 159 | Mouse click and hold


    |   type   | y coordinate
    |----------|-------------------------------------------------------------
    | 0 ~  159 | Mouse click and hold


    ### Reward
    1 if success, otherwise 0.
    """

    def __init__(
        self,
        env_name: str,
        seeds: Union[List[int], None] = None,
        num_instances: int = 1,
        miniwob_dir: str = miniwob_dir,
        headless: bool = False,
    ):
        if seeds is None:
            seeds = [1 for _ in range(num_instances)]

        super().__init__(env_name)
        self.base_url = f"file://{miniwob_dir}"
        self.configure(
            num_instances=num_instances,
            seeds=seeds,
            base_url=self.base_url,
            headless=headless,
        )

        self.obs_im_width = 160
        self.obs_im_height = 210
        self.num_channels = 3  # RGB
        self.obs_im_size = (self.obs_im_width, self.obs_im_height)

        self.obs_im_shape = self.obs_im_size

        self.observation_space = gym.spaces.Box(
            0,
            255,
            (self.obs_im_width, self.obs_im_height, self.num_channels),
            dtype=int,
        )
        self.action_space = gym.spaces.Box(
            low=np.array([0, 0, 0]), high=np.array([2, 159, 159]), shape=(3,), dtype=int
        )

    def reset(
        self,
        seeds: Union[List[int], None] = None,
        mode=None,
        record_screenshots: bool = False,
    ) -> list:
        """Forces stop and start all instances.

        Args:
            seeds (list[object]): Random seeds to set for each instance;
                If specified, len(seeds) must be equal to the number of instances.
                A None entry in the list = do not set a new seed.
            mode (str): If specified, set the data mode to this value before
                starting new episodes.
            record_screenshots (bool): Whether to record screenshots of the states.
        Returns:
            states (list[MiniWoBState])
        """
        # seeds = [1 for _ in range(len(self.instances))]
        miniwob_state = super().reset(seeds, mode, record_screenshots)

        """
        for state in miniwob_state:
            if state:
                state.set_screenshot(
                    state.screenshot.resize(self.obs_im_shape, Image.ANTIALIAS)
                )
        """

        return miniwob_state

    def step(
        self,
        actions,
    ) -> Tuple[List[Image.Image], List[float], List[bool], dict]:
        states, rewards, dones, info = super().step(actions)

        return states, rewards, dones, info


class ReflexionMiniwobEnv(MiniWoBEnvironment):
    def __init__(self, 
                 env_name,
                 miniwob_dir=miniwob_dir,
                 seeds=None,
                 num_instances=1,
                 headless=False):
        super().__init__(env_name)
        
        if seeds is None:
            seeds = [1 for _ in range(num_instances)]

        self.base_url = f"file://{miniwob_dir}"
        self.configure(
            num_instances=num_instances,
            seeds=seeds,
            base_url=self.base_url,
            headless=headless,
        )
        self.reset_flag = True
        
    def reset(self, seeds=None, mode=None, record_screenshots=False):
        self.reset_flag = True
        miniwob_state = super().reset(seeds, mode, record_screenshots)
        return miniwob_state


    def step(self, action, miniwob_action):
        if action == "reset":
            # if self.reset_flag:
            #     instance = self.instances[0]
            #     observation = instance.call(instance.get_state)
            #     qwq = 1
            # else:
            observation = self.reset()[0].html_body
            rewards = [0]
            dones = [False]
        else:
            self.reset_flag = False
            try:
                states, rewards, dones, info = super().step([miniwob_action])
            except Exception as e:
                observation = str(e)
                rewards = [0]
                dones = [False]
            else:
                if dones[0]:
                    observation = f"Your Score: {rewards[0]}"
                else:
                    action_type, action_content = action.split(" ", 1)
                    action_type = action_type.lower()
                    if action_type == "clickxpath":
                        observation = f"youhave clicked xpath {action_content}"
                    elif action_type == "type":
                        observation = f"You have typed {action_content}"
                    else:
                        observation = f"Invalid action {action}"
        return observation, rewards[0], dones[0]


if __name__ == "__main__":
    env = MiniWoBEnv("click-pie")
    for _ in range(1):
        obs = env.reset(record_screenshots=True)

        done = [False]
        while not all(done):
            # Click middle point
            actions = [[0, 80, 140], [1, 80, 140]]
            for action in actions:
                obs, reward, done, info = env.step([action])

            for ob in obs:
                if ob is not None:
                    ob.screenshot.show()
            import time

            time.sleep(3)
    env.close()
