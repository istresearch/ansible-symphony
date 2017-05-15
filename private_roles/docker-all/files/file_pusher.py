import sys
import logging
logger = logging.getLogger(__name__)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
logger.addHandler(ch)


def main():
    import argparse
    from kazoo.client import KazooClient
    import yaml
    import os
    logger.debug("init")
    parser = argparse.ArgumentParser(
            description="Config file pusher to Zookeeper")
    parser.add_argument('-f', '--file', action='store', required=True)
    parser.add_argument('-z', '--zoo-keeper', action='store', required=True,
                        help="The Zookeeper connection <host>:<port>")
    parser.add_argument('-p', '--path', action='store', required=False,
                        default='/grawler')
    parser.add_argument('-e', '--env', action='store', required=False,
                        default='prod')
    args = vars(parser.parse_args())

    filename = args['file']
    zoo = args['zoo_keeper']
    the_path = args['path']
    deploy_env = args['env']

    path = the_path + '/config'
    instance_path = the_path + '/instance'

    zk = KazooClient(hosts=zoo)
    zk.start()

    # ensure path exists
    zk.ensure_path(path)
    zk.ensure_path(instance_path)

    # read whole file
    data = open(filename, 'r').read()
    chunks = data.split('DELIM')
    for i in range(len(chunks)):
        chunks[i] = yaml.load(chunks[i])

    # parse into cleaner dict and sub files
    my_list = []
    for data in chunks:
        id = data['id']
        del data['id']
        file = 'grawler_config.{}.{}.yaml'.format(deploy_env, id)
        my_list.append({
                        'id': str(id),
                        'file': file
                      })

        logger.debug("write file {}".format(file))
        with open(file, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

    # read each sub file, push into zk
    for item in my_list:
        logger.debug("pushing file {}".format(item['file']))
        push(item['file'], path, instance_path, zk, item['id'])

    # clean up temp files
    for item in my_list:
        logger.debug("deleting file {}".format(item['file']))
        os.remove(item['file'])

    zk.stop()


def push(filename, path, instance_path, zk, id):
    bytes = open(filename, 'rb').read()

    # push the conf file
    if not zk.exists(path + '/' + filename):
        logger.debug("creaing conf node")
        zk.create(path + '/' + filename, bytes)
    else:
        logger.debug("updating conf file")
        zk.set(path + '/' + filename, bytes)

    if not zk.exists(instance_path + '/' + id):
        logger.debug("creating id file")
        zk.create(instance_path + '/' + id, '')

    # push the path assignment
    data, stat = zk.get(instance_path + '/' + id)
    if data != path + '/' + filename:
        zk.set(instance_path + '/' + id, path + '/' + filename)
        logger.debug("set assignment")
    else:
        logger.debug("No new assignment")


if __name__ == "__main__":
    sys.exit(main())
