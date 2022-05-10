import asyncio  # 비 동기화 모듈
from bleak import BleakScanner, BleakClient  # BLE 검색 모듈


def on_disconnect(client):
    print("Client with address {} got disconnected!".format(client.address))


def uart_read_callback(sender: int, data: bytearray):
    print('sender: ', sender, 'data: ', data)


# 비동기 형태로 BLE 장치 검색
async def run():
    # 검색 시작 (검색이 종료될 때까지 대기)
    # 기본 검색 시간은 5초이다.
    address = " "
    name = " "
    # address=[]
    # name=[]
    dev_name_uuid = "00002a00-0000-1000-8000-00805f9b34fb"
    uart_write_uuid = "0000fff1-0000-1000-8000-00805f9b34fb"
    uart_read_uuid = "0000fff2-0000-1000-8000-00805f9b34fb"
    while address == " ":
        devices = await BleakScanner.discover(timeout=10.0)
        # 검색된 장치들 리스트 출력
        for d in devices:
            # print(d)
            if d.name == "XRAY_EPD":
                # print(d.name, d.address, d.rssi)
                name = d.name
                address = d.address
                break
    print(name, address)
    # devices = await BleakScanner.discover(timeout=10.0)
    # for d in devices:
    #     if d.name=='XRAY_EPD':
    #         name.append(d.name)
    #         address.append(d.address)
    # print(len(name), address)
    async with BleakClient(address, timeout=10.0) as client:
        client.set_disconnected_callback(on_disconnect)
        read_dev_name = await client.read_gatt_char(dev_name_uuid)
        print(read_dev_name, 'connected')
        await client.start_notify(uart_read_uuid, uart_read_callback)
        await client.write_gatt_char(uart_write_uuid, b'$SGMV#', response=True)
        await asyncio.sleep(1.0)
        await client.stop_notify(uart_read_uuid)

    print('disconnect')


# 비동기 이벤트 루프 생성
loop = asyncio.get_event_loop()
# 비동기 형태로 run(검색)함수 실행
# 완료될 때까지 대기
loop.run_until_complete(run())
print('DONE')
