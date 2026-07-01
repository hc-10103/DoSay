from gymnasium.envs.registration import register

register(
    id="game_env/AppleGame-v0",
    entry_point="game_env.envs:AppleGameEnv"
)