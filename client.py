# Import modul socket untuk membuat server TCP sederhana 
import socket 

# Import modul mimetypes yang digunakan untuk menentukan content type dari suatu file berdasarkan ekstensinya
import mimetypes 

# Membuat fungsi handle_request
def handle_request(request):
    # Memisahkan header dari permintaan
    headers = request.split('\n')
    # Mendapatkan nama file yang diminta dari baris pertama header
    filename = headers[0].split()[1]
    # Jika nama file adalah '/', ganti dengan '/index.html'
    if filename == '/':
        filename = '/index.html'

    try:
        # Membuka file yang diminta dalam mode baca binary
        with open('./html/' + filename, 'rb') as fin:
            # Membaca isi file
            content = fin.read()
        # Menebak jenis konten file menggunakan modul mimetypes
        content_type, _ = mimetypes.guess_type(filename)
        # Membuat header HTTP dengan kode 200 OK dan jenis konten
        headers = f'HTTP/1.0 200 OK\nContent-Type: {content_type}\n\n'.encode()
        # Menggabungkan header dan isi file menjadi respons
        response = headers + content
    except FileNotFoundError:
        # Jika file tidak ditemukan, buat respons dengan kode 404 NOT FOUND
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'.encode()

    return response

def start_server(host, port):

    # Membuat socket server
    # Memanggil socket.socket dari modul socket
    # Panggil dengan parameter socket.AF_INET mengindikasikan penggunaan alamat IPv4
    # Juga socket.SOCK_STREAM menunjukkan penggunaan protokol TCP untuk socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Mengizinkan penggunaan kembali alamat yang sama dengan setsockopt
    # Kemudian mengatur nilai 1 untuk opsi SO_REUSERADDR
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Mengikat socket ke host dan port yang ditentukan
    server_socket.bind((host, port))

    # Mendengarkan koneksi dari client
    server_socket.listen(1)
    
    # Print untuk menandakan bahwa server sedang Listening koneksi dari client
    print(f'Listening sedang berjalan\nHost: {host} \nPort: {port} \n....')

    while True:
        # Menerima koneksi baru dari client
        client_connection, client_address = server_socket.accept()

        # Menerima permintaan data dari client dengan recv
        request = client_connection.recv(1024).decode()

        # Menampilkan permintaan apa saja yang terjadi agar mudah dalam pemantauan
        print(request)

        # Memanggil fungsi handle_request untuk memproses permintaan dan mendapatkan respons
        response = handle_request(request)

        # Mengirimkan respons dari server ke client berdasarkan hasil olah response pada fungsi handle_request
        client_connection.sendall(response)

        # Menutup koneksi dengan client untjk mengakhiri sesi listening dan membebaskan resource
        client_connection.close()


# Membuat fungsi main
def main():
    host = 'localhost'  # Inisialisasi 'localhost' sebagai alamat host
    port = 1831  # Inisialisasi 1831 sebagai alamat port
    
    # Memulai server dengan host dan port yang ditentukan
    start_server(host, port)

# Memanggil fungsi main
main()