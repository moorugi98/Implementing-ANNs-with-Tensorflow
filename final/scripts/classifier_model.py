import tensorflow as tf

# TODO: optimize the architecture of classifier
def get_classifier(c_dim, num_classes):
    embedding_inputs = tf.keras.Input(shape=(c_dim))
    x = tf.keras.layers.Dense(64, activation="relu")(embedding_inputs)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dense(256, activation="relu")(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    model = tf.keras.Model(inputs=embedding_inputs, outputs=outputs, name="music_classifier")
    return model
