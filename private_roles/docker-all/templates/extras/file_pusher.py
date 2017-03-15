import sys

def main():
    import argparse
    from kazoo.client import KazooClient

    parser = argparse.ArgumentParser(
            description="Config file pusher to Zookeeper")
    parser.add_argument('-f', '--file', action='store', required=True)
    parser.add_argument('-i', '--id', action='store', default='000')
    parser.add_argument('-w', '--wipe', action='store_const', const=True)
    parser.add_argument('-z', '--zoo-keeper', action='store', required=True,
                        help="The Zookeeper connection <host>:<port>")
    args = vars(parser.parse_args())

    filename = args['file']
    id = args['id']
    wipe = args['wipe']
    zoo = args['zoo_keeper']

    path = '/scrapy-cluster/indexer'
    path2 = '/scrapy-cluster/indexer_conf'

    zk = KazooClient(hosts=zoo)
    zk.start()

    # ensure path exists
    zk.ensure_path(path)
    zk.ensure_path(path2)

    bytes = open(filename, 'rb').read()

    # push the conf file
    if not zk.exists(path2 + '/' + filename):
        print "creaing conf node"
        zk.create(path2 + '/' + filename, bytes)
    else:
        print "updating conf file"
        zk.set(path2 + '/' + filename, bytes)

    if id and zk.exists(path + '/' + id):
        # push the path assignment
        data, stat = zk.get(path + '/' + id)
        if wipe:
            zk.set(path + '/' + id, None)
        elif data != path2 + filename:
            zk.set(path + '/' + id, path2 + '/' + filename)
        else:
            print "No new assignment"
    elif id:
        print "No indexer with id", id


    zk.stop()

if __name__ == "__main__":
    sys.exit(main())
