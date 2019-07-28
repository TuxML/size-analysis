from feature_selection import FeaturesLoader
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

class NetLauncher(object):

    def __init__(self, name_csv = 'feature_importanceRF.csv', predict_var ='vmlinux', drop_feature = True,
                 nb_features = 1000, learning_rate1 = 0.5, learning_rate2 = 0.025, nb_node_layer1 = 200,
                 nb_node_layer2 = 300, batch_size = 50, nb_epochs = 30, training_size = 0.9):

        f = FeaturesLoader(predict_var = predict_var, name_csv = name_csv, nb_features = nb_features, drop_feature = drop_feature)

        self.features = f.get_selected_features()

        self.predict_var = predict_var
        self.learning_rate1 = learning_rate1
        self.learning_rate2 = learning_rate2
        self.nb_node_layer1 = nb_node_layer1
        self.nb_node_layer2 = nb_node_layer2
        self.batch_size = batch_size
        self.nb_epochs = nb_epochs
        self.training_size = training_size

    def create_train_test_set(self):

        n = 65000
        sizes = np.array(self.features[0:n][self.predict_var])
        x_train, x_test, y_train, y_test = train_test_split(self.features.drop(self.predict_var, axis=1)[0:n], sizes, test_size = 1-self.training_size)

        x_train = np.array(x_train, dtype = np.float32)
        x_test =  np.array(x_test, dtype = np.float32)

        y_train = np.array(y_train, dtype = np.float32)
        y_test = np.array(y_test, dtype = np.float32)

        return (x_train, y_train, x_test, y_test)

    def compute_tiny(self):
        #, batch_size=20, nb_epochs=5, learning_rate=1000):

        batch_size = self.batch_size
        nb_epochs = self.nb_epochs
        learning_rate = self.learning_rate

        training_x, training_y, testing_x, testing_y = self.create_train_test_set()

        nb_features = training_x.shape[1]
        nb_batch_train = int(len(training_x) / batch_size)
        nb_batch_test = int(len(testing_x) / batch_size)

        dataset_train = tf.data.Dataset.from_tensor_slices((training_x, training_y)).batch(batch_size)
        iterator_train = tf.compat.v1.data.make_initializable_iterator(dataset_train)
        xtr, ytr = iterator_train.get_next()

        dataset_test = tf.data.Dataset.from_tensor_slices((testing_x, testing_y)).batch(batch_size)
        iterator_test = tf.compat.v1.data.make_initializable_iterator(dataset_test)
        xte, yte = iterator_test.get_next()

        with tf.device("/gpu:0"):

            w_h1 = tf.Variable(tf.glorot_uniform_initializer()((nb_features, 1)))

            outputs_tr = tf.reshape(tf.matmul(xtr, w_h1), shape=[batch_size])
            ytr = tf.reshape(ytr, [batch_size])

            outputs_te = tf.reshape(tf.matmul(xte, w_h1), shape=[batch_size])
            yte = tf.reshape(yte, [batch_size])

            train_cost = tf.keras.losses.MAPE(ytr, outputs_tr)
            test_cost = tf.keras.losses.MAPE(yte, outputs_te)

            train_step = tf.train.AdamOptimizer(learning_rate).minimize(train_cost)

            init = tf.global_variables_initializer()

        with tf.Session() as sess:
            sess.run(init)
            for ep in range(nb_epochs):
                sess.run(iterator_train.initializer)
                for i in range(nb_batch_train):
                    val = sess.run(train_step)
            mape_train = 0
            sess.run(iterator_train.initializer)
            for i in range(nb_batch_train):
                mape_train += sess.run(train_cost)
            print("Training final cost =", mape_train / nb_batch_train)
            mape_test = 0
            sess.run(iterator_test.initializer)
            for i in range(nb_batch_test):
                mape_test += sess.run(test_cost)
            print("Test final cost =", mape_test / nb_batch_test)
            return (mape_train / nb_batch_train, mape_test / nb_batch_test)

    def compute_small(self):
            #batch_size=20, nb_epochs=5, learning_rate=10, nb_node_layer1=200):

        batch_size = self.batch_size
        nb_epochs = self.nb_epochs
        learning_rate = self.learning_rate
        nb_node_layer1 = self.nb_node_layer1
        training_x, training_y, testing_x, testing_y = self.create_train_test_set()

        nb_features = training_x.shape[1]
        nb_batch_train = int(len(training_x) / batch_size)
        nb_batch_test = int(len(testing_x) / batch_size)

        dataset_train = tf.data.Dataset.from_tensor_slices((training_x, training_y)).batch(batch_size)
        iterator_train = tf.compat.v1.data.make_initializable_iterator(dataset_train)
        xtr, ytr = iterator_train.get_next()

        dataset_test = tf.data.Dataset.from_tensor_slices((testing_x, testing_y)).batch(batch_size)
        iterator_test = tf.compat.v1.data.make_initializable_iterator(dataset_test)
        xte, yte = iterator_test.get_next()

        with tf.device("/gpu:0"):
            w_h1_tr = tf.Variable(tf.glorot_uniform_initializer()((nb_features, nb_node_layer1)), name="w_h1_tr")
            mat_h1_tr = tf.matmul(xtr, w_h1_tr)
            b_h1_tr = tf.Variable(tf.zeros(nb_node_layer1), name="b_h1_tr")
            out_h1_tr = tf.nn.relu(tf.add(mat_h1_tr, b_h1_tr))

            mat_h1_te = tf.matmul(xte, w_h1_tr)
            out_h1_te = tf.nn.relu(tf.add(mat_h1_te, b_h1_tr))

            w_h2 = tf.Variable(tf.glorot_uniform_initializer()((nb_node_layer1, 1)))

            outputs_tr = tf.reshape(tf.matmul(out_h1_tr, w_h2), shape=[batch_size])
            ytr = tf.reshape(ytr, [batch_size])

            outputs_te = tf.reshape(tf.matmul(out_h1_te, w_h2), shape=[batch_size])
            yte = tf.reshape(yte, [batch_size])

            train_cost = tf.keras.losses.MAPE(ytr, outputs_tr)
            test_cost = tf.keras.losses.MAPE(yte, outputs_te)

            train_step = tf.train.AdamOptimizer(learning_rate).minimize(train_cost)

            init = tf.global_variables_initializer()

        with tf.Session() as sess:
            sess.run(init)
            for ep in range(nb_epochs):
                sess.run(iterator_train.initializer)
                for i in range(nb_batch_train):
                    val = sess.run(train_step)
            mape_train = 0
            sess.run(iterator_train.initializer)
            for i in range(nb_batch_train):
                mape_train += sess.run(train_cost)
            print("Training final cost =", mape_train / nb_batch_train)
            mape_test = 0
            sess.run(iterator_test.initializer)
            for i in range(nb_batch_test):
                mape_test += sess.run(test_cost)
            print("Test final cost =", mape_test / nb_batch_test)
            return (mape_train / nb_batch_train, mape_test / nb_batch_test)


    def compute_standard(self):

        batch_size = self.batch_size
        nb_epochs = self.nb_epochs
        learning_rate1 = self.learning_rate1
        learning_rate2 = self.learning_rate2
        nb_node_layer1 = self.nb_node_layer1
        nb_node_layer2 = self.nb_node_layer2
        training_x, training_y, testing_x, testing_y = self.create_train_test_set()

        nb_features = training_x.shape[1]
        nb_batch_train = int(len(training_x) / batch_size)
        nb_batch_test = int(len(testing_x) / batch_size)

        # slice the datasets => feed_dict was very slow, so I choose an iterator solution
        dataset_train = tf.data.Dataset.from_tensor_slices((training_x, training_y)).batch(batch_size)
        iterator_train = tf.compat.v1.data.make_initializable_iterator(dataset_train)
        xtr, ytr = iterator_train.get_next()

        dataset_test = tf.data.Dataset.from_tensor_slices((testing_x, testing_y)).batch(batch_size)
        iterator_test = tf.compat.v1.data.make_initializable_iterator(dataset_test)
        xte, yte = iterator_test.get_next()

        with tf.device("/gpu:0"):
            # Layers training
            w_h1_tr = tf.Variable(tf.glorot_uniform_initializer()((nb_features, nb_node_layer1)), name="w_h1_tr")
            mat_h1_tr = tf.matmul(xtr, w_h1_tr)
            b_h1_tr = tf.Variable(tf.zeros(nb_node_layer1), name="b_h1_tr")
            out_h1_tr = tf.nn.relu(tf.add(mat_h1_tr, b_h1_tr))

            w_h2_tr = tf.Variable(tf.glorot_uniform_initializer()((nb_node_layer1, nb_node_layer2)), name="w_h2_tr")
            mat_h2_tr = tf.matmul(out_h1_tr, w_h2_tr)
            b_h2_tr = tf.Variable(tf.zeros(nb_node_layer2), name="b_h2_tr")
            out_h2_tr = tf.nn.relu(tf.add(mat_h2_tr, b_h2_tr))

            w_final_tr = tf.Variable(tf.glorot_uniform_initializer()((nb_node_layer2, 1)), name="w_final_tr")
            outputs_tr = tf.reshape(tf.matmul(out_h2_tr, w_final_tr), shape=[batch_size])
            ytr = tf.reshape(ytr, [batch_size])

            # Layers test
            mat_h1_te = tf.matmul(xte, w_h1_tr)
            out_h1_te = tf.nn.relu(tf.add(mat_h1_te, b_h1_tr))

            mat_h2_te = tf.matmul(out_h1_te, w_h2_tr)
            out_h2_te = tf.nn.relu(tf.add(mat_h2_te, b_h2_tr))

            outputs_te = tf.reshape(tf.matmul(out_h2_te, w_final_tr), shape=[batch_size])
            yte = tf.reshape(yte, [batch_size])

            # Cost => MAPE
            train_cost = tf.keras.losses.MAPE(ytr, outputs_tr)
            test_cost = tf.keras.losses.MAPE(yte, outputs_te)

            # Convergence function => AdamOptimizer
            train_step = tf.train.AdamOptimizer(learning_rate=learning_rate1).minimize(train_cost)

            # train step with a lower learning rate => gain few % at the end
            tiny_train_step = tf.train.AdamOptimizer(learning_rate=learning_rate2).minimize(train_cost)

            # allocate memory for tensors
            init = tf.global_variables_initializer()

        with tf.Session() as sess:
            sess.run(init)
            for j in range(nb_epochs):
                if j < 20:
                    sess.run(iterator_train.initializer)
                    for i in range(nb_batch_train):
                        val = sess.run(train_step)
                    # print("Train epoch n°", j+1, ":",  sess.run(train_cost))
                else:
                    sess.run(iterator_train.initializer)
                    for i in range(nb_batch_train):
                        val = sess.run(tiny_train_step)
                    # print("Train epoch n°", j+1, ":",  sess.run(train_cost))
            sess.run(iterator_train.initializer)
            mape_train = 0
            for i in range(nb_batch_train):
                mape_train += sess.run(train_cost)
            print("Training final cost =", mape_train / nb_batch_train)
            mape_test = 0
            sess.run(iterator_test.initializer)
            for i in range(nb_batch_test):
                mape_test += sess.run(test_cost)
            print("Test final cost =", mape_test / nb_batch_test)
            return (mape_train / nb_batch_train, mape_test / nb_batch_test)

    def launch(self):
        if self.training_size < float(1/65):
            return self.compute_tiny()
        if self.training_size > float(1/65) and self.training_size < float(10/65):
            return self.compute_small()
        return self.compute_standard()