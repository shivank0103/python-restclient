from client import RestClient


def t1():
    internal_client = RestClient(
        app_name='customer', service_name='buyback',
        etcd_host='etcd.prv.api.stage.cashify.in', etcd_protocol='http', etcd_port=80
    )
    # https://caddy.community/t/using-zerossls-acme-endpoint/9406

    client = RestClient(base_url='https://caddy.community')
    print(client.response('GET', 't/using-zerossls-acme-endpoint/9406'))

    print(internal_client.response('GET', 'v1/health'))


if __name__ == '__main__':
    t1()
