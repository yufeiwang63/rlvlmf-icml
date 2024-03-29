python train_PEBBLE.py \
    env=metaworld_drawer-open-v2 \
    seed=1 \
    reward=learn_from_preference \
    vlm_label=1 \
    vlm=gemini_free_form \
    image_reward=1 \
    reward_batch=40 \
    segment=1 \
    teacher_eps_mistake=0 \
    flip_vlm_label=0 \
    reward_update=10 \
    num_interact=4000 \
    max_feedback=20000 \
    agent.params.actor_lr=0.0003 agent.params.critic_lr=0.0003 gradient_update=1 activation=tanh num_unsup_steps=9000 \
    num_train_steps=1000000 agent.params.batch_size=512 double_q_critic.params.hidden_dim=256 double_q_critic.params.hidden_depth=3 \
    diag_gaussian_actor.params.hidden_dim=256 diag_gaussian_actor.params.hidden_depth=3  \
    feed_type=0 teacher_beta=-1 teacher_gamma=1  teacher_eps_skip=0 teacher_eps_equal=0 \
    num_eval_episodes=1

