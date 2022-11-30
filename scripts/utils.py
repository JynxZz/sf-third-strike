from google.cloud import storage

# import de diff settings pour les params

import numpy as np
import random
import pickle
import json
import os
import datetime

init_timestamp = datetime.now()

LOCAL_PATH=os.environ.get('LOCAL_PATH')
LOCAL_FILENAME=os.environ.get('LOCAL_FILENAME')


# TODO : Local
def local_save(data, file_name=LOCAL_FILENAME):
        weights_folder_path = LOCAL_PATH
        if not os.path.exists(weights_folder_path):
            os.makedirs(weights_folder_path)

        file_name = os.path.join(weights_folder_path, file_name)
        with open(file_name, 'w') as f:
            f.write(data)

def local_read(file_name=LOCAL_FILENAME):
    weights_folder_path = LOCAL_PATH
    file_name = os.path.join(weights_folder_path, file_name)

    with open(file_name, 'r') as f:
        f.readlines()

    return f



def creation_date(path_to_file):
    try:

        return os.path.getctime(path_to_file)
    except:

        pass


# TODO : switch client / server done
def switch(old_timestamp):

    timestamp = creation_date()

    if old_timestamp < timestamp:
        old_timestamp = timestamp
        return old_timestamp, True

    return old_timestamp, False


# TODO : Connect to the bucket : OK

# TODO : Save weights inside bucket : WIP -> good path ...
def bucket_save(file):

    client = storage.Client(project=os.environ.get('PROJECT'))
    bucket = client.bucket(os.environ.get('BUCKET_TEST'))
    blob = bucket.blob(f"{os.environ.get('STORAGE_LOCATION')}/{file}")

    blob.upload_from_filename(file)

# TODO : Load weigths inside bucket : OK
def load_weights(file):

    client = storage.Client()
    bucket = client.bucket(os.environ.get('BUCKET'))
    blob = bucket.blob(os.environ.get('STORAGE_LOCATION'))

    blob.download_to_filename(file)

    return blob


def extract_buffer(client_agent):
    #Extracting buffer
    buffer = client_agent.rollout_buffer
    observation = buffer.observations
    action = buffer.actions
    reward = buffer.rewards
    episode_start = buffer.episode_starts
    value = buffer.values
    log_prob = buffer.log_probs

    to_buffer = (observation, action,
                 reward, episode_start,
                 value, log_prob,
                 buffer.returns, buffer.advantages)
    return to_buffer


def concat_buffer(buffers):
    #Stack buffers
    assert len(buffers)>2, "No buffer to add"
    n=len(buffers)
    init = buffers[0]
    a, b, c, d, e, f, g, h = init
    # a = init[0]
    # b = init[1]
    # c = init[2]
    # d = init[3]
    # e = init[4]
    # f = init[5]
    # g = init[6]
    # h = init[7]
    #print(np.vstack([b,buffers[1][1]]))
    for j in range(n-1):
        b = np.vstack([b,buffers[j+1][1]])
        c = np.vstack([c,buffers[j+1][2]])
        d = np.vstack([d,buffers[j+1][3]])
        e = np.vstack([e,buffers[j+1][4]])
        f = np.vstack([f,buffers[j+1][5]])
        g = np.vstack([g,buffers[j+1][6]])
        h = np.vstack([h,buffers[j+1][7]])

        for key in init[0].keys():
            a[key]=np.vstack([a[key],buffers[j+1][0][key]])

    return (a,b,c,d,e,f,g,h)


def import_buffer(imported_obs, server_agent):

    server_agent.rollout_buffer.reset()
    server_agent.rollout_buffer.buffer_size = server_agent.n_steps
    server_agent.rollout_buffer.observations = imported_obs[0]
    server_agent.rollout_buffer.actions = imported_obs[1]
    server_agent.rollout_buffer.rewards = imported_obs[2]
    server_agent.rollout_buffer.episode_starts = imported_obs[3]
    server_agent.rollout_buffer.values = imported_obs[4]
    server_agent.rollout_buffer.log_probs = imported_obs[5]
    server_agent.rollout_buffer.returns = imported_obs[6]
    server_agent.rollout_buffer.advantages = imported_obs[7]
    server_agent.rollout_buffer.generator_ready = True
    server_agent.rollout_buffer.pos=len(imported_obs[5])
    server_agent.rollout_buffer.full=True
    # logg = configure(folder='/tmp/')
    # server_agent.set_logger(logg)

    return server_agent



if __name__ == '__main__':
    #  local_save('coucou')
    print(creation_date("weights-agent-two.txt"))
