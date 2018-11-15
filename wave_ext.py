import wave
import struct

# Todo Add insert
class ReadWriteWav:
    """
    Opens a wav file to be edited.
    Make shore to call close when finished.
    """

    sample_data = []

    def __init__(self, read_filename=None):
        """Initialize readWriteWav
        :param read_filename: if none creates an empty array to stream to.
        """
        self.sample_data = []
        if read_filename is not None:
            self.get_sample_data(read_filename)

    def get_sample_data(self, filename):
        """reads sample data from file and stores it as an int value in
        sample_data and fills to the length required for saving"""

        # clear the sample data incase its being changed
        self.sample_data = []

        read_file = wave.open(filename+".wav", "rb")
        total_samples = read_file.getnframes()

        # get all the date from the file in an editable format
        # for the length of max length.
        for i in range(total_samples):
                sample_byte = read_file.readframes(1)
                self.sample_data.append(ReadWriteWav.sample_byte_to_value(sample_byte))

        read_file.close()

    @staticmethod
    def open_write_wav_file(filename):
        """does not require the .wav extension"""
        return wave.open(filename+".wav", "w")

    @staticmethod
    def sample_byte_to_value(sample_byte):
        """
        get the sample value from byte
        :param sample_byte:     should be a tuple of 1
        :return:                human friendly value (int)
        """
        if sample_byte != b'':
            return struct.unpack_from('h', sample_byte)[0]
        else:
            return 0

    @staticmethod
    def sample_value_to_byte(sample_value):
        return struct.pack('h', int(sample_value))

    def get_sample_at_position(self, position):

        return self.sample_data[position]

    def get_sample_range(self, start_position, length):

        return self.sample_data[start_position:(start_position+length)]

    def add_sample(self, value):

        self.sample_data.append(value)

    def set_sample(self, sample_numb, value):

        self.sample_data[sample_numb] = value

    def combine_samples(self, sample_numb, value):

        self.sample_data[sample_numb] += value

    def normalize(self, max_depth):

        max_samp = 0;
        for samp in self.sample_data:
            if self.abs(samp) > max_samp:
                max_samp = self.abs(samp)

        amplification = float(max_depth) / max_samp

        out_max = 0

        for i in range(len(self.sample_data)):
            louder = int(self.sample_data[i] * amplification)
            self.sample_data[i] = louder
            if louder > out_max:
                out_max = louder


    @staticmethod
    def abs(value):
        if value < 0:
            return -value

        return value


    def write_sample_data(self, filename, channels=1, sample_rate=44100):

        write_file = ReadWriteWav.open_write_wav_file(filename)
        write_file.setparams(
            (channels, 2, sample_rate,
             len(self.sample_data), "NONE", "not compressed")
        )

        byte_data = []

        # convert sample data into bytes
        for sample in self.sample_data:
            byte_data.append(ReadWriteWav.sample_value_to_byte(sample))

        byte_str = b''.join(byte_data)
        write_file.writeframesraw(byte_str)

        write_file.close()

        print(filename, "file saved")