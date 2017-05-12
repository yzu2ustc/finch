import tensorflow as tf


class MLP_GAN:
    def __init__(self, n_G_in, n_D_in, lr_G=1e-4, lr_D=1e-4):
        self.n_G_in = n_G_in
        self.n_D_in = n_D_in
        self.lr_G = lr_G
        self.lr_D = lr_D
        self.build_graph()
    # end constructor


    def build_graph(self):
        with tf.variable_scope('G'):
            self.add_Generator()
        with tf.variable_scope('D'):
            self.add_Discriminator()
        self.add_backward_path()
    # end method build_graph


    def add_Generator(self):
        self.G_in = tf.placeholder(tf.float32, [None, self.n_G_in])
        G_hidden = tf.layers.dense(self.G_in, 128, tf.nn.relu)
        self.G_out = tf.layers.dense(G_hidden, self.n_D_in)
    # end method add_Generator


    def add_Discriminator(self):
        self.D_in = tf.placeholder(tf.float32, [None, self.n_D_in]) # real data
        D_hidden = tf.layers.dense(self.D_in, 128, tf.nn.relu, name='hidden')
        self.D_prob = tf.layers.dense(D_hidden, 1, tf.nn.sigmoid, name='out')
        D_hidden = tf.layers.dense(self.G_out, 128, tf.nn.relu, name='hidden', reuse=True)
        self.G_prob = tf.layers.dense(D_hidden, 1, tf.nn.sigmoid, name='out', reuse=True)
    # end method add_Discriminator


    def add_backward_path(self):
        self.G_loss = tf.reduce_mean(tf.log(1 - self.G_prob))
        self.D_loss = - tf.reduce_mean(tf.log(self.D_prob) + tf.log(1 - self.G_prob))
        self.G_train = tf.train.AdamOptimizer(self.lr_G).minimize(self.G_loss,
            var_list=tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='G'))
        self.D_train = tf.train.AdamOptimizer(self.lr_D).minimize(self.D_loss,
            var_list=tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='D'))
    # end method add_backward_path
# end class