using System;
using System.Diagnostics;
using Windows.Foundation;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Navigation;

// This is the click handler for the 'Copy Strings' button.  Here we will parse the
// strings contained in the ElementsToWrite text block, write them to a stream using
// DataWriter, retrieve them using DataReader, and output the results in the
// ElementsRead text block.
private async void TransferData(object sender, RoutedEventArgs e)
{
    // Initialize the in-memory stream where data will be stored.
    using (var stream = new Windows.Storage.Streams.InMemoryRandomAccessStream())
    {
        // Create the data writer object backed by the in-memory stream.
        using (var dataWriter = new Windows.Storage.Streams.DataWriter(stream))
        {
            dataWriter.UnicodeEncoding = Windows.Storage.Streams.UnicodeEncoding.Utf8;
            dataWriter.ByteOrder = Windows.Storage.Streams.ByteOrder.LittleEndian;

            // Parse the input stream and write each element separately.
            string[] inputElements = ElementsToWrite.Text.Split(';');
            foreach (string inputElement in inputElements)
            {
                uint inputElementSize = dataWriter.MeasureString(inputElement);
                dataWriter.WriteUInt32(inputElementSize);
                dataWriter.WriteString(inputElement);
            }

            // Send the contents of the writer to the backing stream.
            await dataWriter.StoreAsync();

            // For the in-memory stream implementation we are using, the flushAsync call 
            // is superfluous,but other types of streams may require it.
            await dataWriter.FlushAsync();

            // In order to prolong the lifetime of the stream, detach it from the 
            // DataWriter so that it will not be closed when Dispose() is called on 
            // dataWriter. Were we to fail to detach the stream, the call to 
            // dataWriter.Dispose() would close the underlying stream, preventing 
            // its subsequent use by the DataReader below.
            dataWriter.DetachStream();
        }

        // Create the input stream at position 0 so that the stream can be read 
        // from the beginning.
        using (var inputStream = stream.GetInputStreamAt(0))
        {
            using (var dataReader = new Windows.Storage.Streams.DataReader(inputStream))
            {
                // The encoding and byte order need to match the settings of the writer 
                // we previously used.
                dataReader.UnicodeEncoding = Windows.Storage.Streams.UnicodeEncoding.Utf8;
                dataReader.ByteOrder = Windows.Storage.Streams.ByteOrder.LittleEndian;

                // Once we have written the contents successfully we load the stream.
                await dataReader.LoadAsync((uint)stream.Size);

                var receivedStrings = "";

                // Keep reading until we consume the complete stream.
                while (dataReader.UnconsumedBufferLength > 0)
                {
                    // Note that the call to readString requires a length of "code units" 
                    // to read. This is the reason each string is preceded by its length 
                    // when "on the wire".
                    uint bytesToRead = dataReader.ReadUInt32();
                    receivedStrings += dataReader.ReadString(bytesToRead) + "\n";
                }

                // Populate the ElementsRead text block with the items we read 
                // from the stream.
                ElementsRead.Text = receivedStrings;
            }
        }
    }
}

// using System;
// using System.Threading.Tasks;
// using Windows.Devices.Bluetooth.Rfcomm;
// using Windows.Networking.Sockets;
// using Windows.Storage.Streams;
// using Windows.Devices.Bluetooth;

// Windows.Devices.Bluetooth.Rfcomm.RfcommDeviceService _service;
// Windows.Networking.Sockets.StreamSocket _socket;

// async void Initialize()
// {
//     // Enumerate devices with the object push service
//     var services =
//         await Windows.Devices.Enumeration.DeviceInformation.FindAllAsync(
//             RfcommDeviceService.GetDeviceSelector(
//                 RfcommServiceId.ObexObjectPush));

//     if (services.Count > 0)
//     {
//         // Initialize the target Bluetooth BR device
//         var service = await RfcommDeviceService.FromIdAsync(services[0].Id);

//         bool isCompatibleVersion = await IsCompatibleVersionAsync(service);

//         // Check that the service meets this App's minimum requirement
//         if (SupportsProtection(service) && isCompatibleVersion)
//         {
//             _service = service;

//             // Create a socket and connect to the target
//             _socket = new StreamSocket();
//             await _socket.ConnectAsync(
//                 _service.ConnectionHostName,
//                 _service.ConnectionServiceName,
//                 SocketProtectionLevel
//                     .BluetoothEncryptionAllowNullAuthentication);

//             // The socket is connected. At this point the App can wait for
//             // the user to take some action, for example, click a button to send a
//             // file to the device, which could invoke the Picker and then
//             // send the picked file. The transfer itself would use the
//             // Sockets API and not the Rfcomm API, and so is omitted here for
//             // brevity.
//         }
//     }
// }

// // This App requires a connection that is encrypted but does not care about
// // whether it's authenticated.
// bool SupportsProtection(RfcommDeviceService service)
// {
//     switch (service.ProtectionLevel)
//     {
//         case SocketProtectionLevel.PlainSocket:
//             if ((service.MaxProtectionLevel == SocketProtectionLevel
//                     .BluetoothEncryptionWithAuthentication)
//                 || (service.MaxProtectionLevel == SocketProtectionLevel
//                     .BluetoothEncryptionAllowNullAuthentication))
//             {
//                 // The connection can be upgraded when opening the socket so the
//                 // App may offer UI here to notify the user that Windows may
//                 // prompt for a PIN exchange.
//                 return true;
//             }
//             else
//             {
//                 // The connection cannot be upgraded so an App may offer UI here
//                 // to explain why a connection won't be made.
//                 return false;
//             }
//         case SocketProtectionLevel.BluetoothEncryptionWithAuthentication:
//             return true;
//         case SocketProtectionLevel.BluetoothEncryptionAllowNullAuthentication:
//             return true;
//     }
//     return false;
// }

// // This App relies on CRC32 checking available in version 2.0 of the service.
// const uint SERVICE_VERSION_ATTRIBUTE_ID = 0x0300;
// const byte SERVICE_VERSION_ATTRIBUTE_TYPE = 0x0A;   // UINT32
// const uint MINIMUM_SERVICE_VERSION = 200;
// async Task<bool> IsCompatibleVersionAsync(RfcommDeviceService service)
// {
//     var attributes = await service.GetSdpRawAttributesAsync(
//         BluetoothCacheMode.Uncached);
//     var attribute = attributes[SERVICE_VERSION_ATTRIBUTE_ID];
//     var reader = DataReader.FromBuffer(attribute);

//     // The first byte contains the attribute's type
//     byte attributeType = reader.ReadByte();
//     if (attributeType == SERVICE_VERSION_ATTRIBUTE_TYPE)
//     {
//         // The remainder is the data
//         uint version = reader.ReadUInt32();
//         return version >= MINIMUM_SERVICE_VERSION;
//     }
//     else return false;
// }