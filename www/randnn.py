import tensorflow as tf

fixtures_files = tf.train.string_input_producer(["fixtures_1.csv"])
reader = tf.TextLineReader()
key, value = reader.read(fixtures_files)

record_defaults = [[1], [1], [1]]
col1, col2, col3 = tf.decode_csv(value, record_defaults=record_defaults)
features = tf.stack([col1, col2])

with tf.Session() as sess:
  # Start populating the filename queue.
  coord = tf.train.Coordinator()
  threads = tf.train.start_queue_runners(coord=coord)

  for i in range(10):
    # Retrieve a single instance:
    example, label = sess.run([features, col3])
    print example
    print label
    print sess.run(reader.num_records_produced())

    sess.run(reader.reset())

  coord.request_stop()
  coord.join(threads)