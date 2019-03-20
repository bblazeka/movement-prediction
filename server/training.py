import pickle
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import scale
import keras
from keras.models import Sequential
from keras.optimizers import SGD, Adam, Adagrad
from keras import backend as K
from keras import layers, models
from keras.layers.embeddings import Embedding
from keras.layers import Concatenate, Input
from keras.layers.core import Dense, Reshape, Activation, Dropout
from keras.callbacks import ModelCheckpoint
from utils import tf_haversine
from data import load_data
from utils import get_clusters


def start_new_session():
    """
    Starts a new Tensorflow session.
    """
    
    # Make sure the session only uses the GPU memory that it actually needs
    config = tf.ConfigProto(gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=0.1))
    
    session = tf.Session(config=config, graph=tf.get_default_graph())
    K.tensorflow_backend.set_session(session)


def first_last_k(coords):
    """
    Returns a list with the first k and last k GPS coordinates from the given trip.
    The returned list contains 4k values (latitudes and longitudes for 2k points).
    """
    k = 5
    partial = [coords[0] for i in range(2*k)]
    num_coords = len(coords)
    if num_coords < 2*k:
        partial[-num_coords:] = coords
    else:
        partial[:k] = coords[:k]
        partial[-k:] = coords[-k:]
    partial = np.row_stack(partial)
    return np.array(partial).flatten()


def process_features(df):
    """
    Process the features required by our model from the given dataframe.
    Return the features in a list so that they can be merged in our model's input layer.
    """
    # Fetch the first and last GPS coordinates
    coords = np.row_stack(df['POLYLINE'].apply(first_last_k))
    # Standardize latitudes (odd columns) and longitudes (even columns)
    latitudes = coords[:,::2]
    coords[:,::2] = scale(latitudes)
    longitudes = coords[:,1::2]
    coords[:,1::2] = scale(longitudes)
    
    return [
        coords,
    ]


def create_model(metadata, clusters):
    """
    Creates all the layers for our neural network model.
    """
      
    # Arbitrary dimension for all embeddings
    embedding_dim = 10
    
    # GPS coordinates (5 first lat/long and 5 latest lat/long, therefore 20 values)
    model = Sequential()
    model.add(Dense(1, input_dim=20, kernel_initializer='normal'))

    # Simple hidden layer
    model.add(Dense(500))
    model.add(Activation('relu'))

    # Determine cluster probabilities using softmax
    model.add(Dense(len(clusters)))
    model.add(Activation('softmax'))

    # Final activation layer: calculate the destination as the weighted mean of cluster coordinates
    cast_clusters = K.cast_to_floatx(clusters)
    def destination(probabilities):
        return tf.matmul(probabilities, cast_clusters)
    model.add(Activation(destination))

    # Compile the model
    optimizer = SGD(lr=0.01, momentum=0.9, clipvalue=1.)  # Use `clipvalue` to prevent exploding gradients
    model.compile(loss=tf_haversine, optimizer=optimizer)
    
    return model


def full_train(n_epochs=100, batch_size=200, save_prefix=None):
    """
    Runs the complete training process.
    """
    
    # Load initial data
    print("Loading data...")
    data = load_data()

    # Estimate the GPS clusters
    print("Estimating clusters...")
    clusters = get_clusters(data.train_labels)
    
    # Set up callbacks
    callbacks = []
    if save_prefix is not None:
        # Save the model's intermediary weights to disk after each epoch
        file_path="cache/%s-{epoch:03d}-{val_loss:.4f}.hdf5" % save_prefix
        callbacks.append(ModelCheckpoint(file_path, monitor='val_loss', mode='min', save_weights_only=True, verbose=1))

    # Create model
    print("Creating model...")
    start_new_session()
    model = create_model(data.metadata, clusters)

    # Run the training
    print("Start training...")
    history = model.fit(
        process_features(data.train), data.train_labels,
        epochs=n_epochs, batch_size=batch_size,
        validation_data=(process_features(data.validation), data.validation_labels),
        callbacks=callbacks)

    if save_prefix is not None:
        # Save the training history to disk
        file_path = 'cache/%s-history.pickle' % save_prefix
        with open(file_path, 'wb') as handle:
            pickle.dump(history.history, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    return history