class BinaryWriter:
    def __init__(self, fp, binary_metadata):
        self.fp = fp
        self.binary_metadata = binary_metadata
        self.encoding = 'ascii'

    def int_to_bytes(self, width, value):
        byte_order_name = self.binary_metadata.byte_order
        byte_order = {'le': 'little', 'be': 'big'}[byte_order_name]
        return value.to_bytes(width, byte_order, signed=True)

    def write_instruction(self, instruction):
        if instruction.prototype is None:
            raise RuntimeError('instruction instance not linked to prototype')

        buffer = bytearray()
        # add instruction id
        iid = instruction.prototype.bin_id
        buffer.extend(self.iid_to_bytes(iid))
        # add values to buffer
        for val in instruction.val_list:
            buffer.extend(self.val_to_bytes(val))

        self.fp.write(buffer)

    def write_binary_metadata(self, instruction_list, meta_attrs):
        instruction_count = len(instruction_list)
        param_count = sum([len(instruction.val_list)
                           for instruction in instruction_list])

        buffer = bytearray()
        # add signature, offset +0x00
        buffer.extend(bytes(self.binary_metadata.signature, encoding='ascii'))
        # add instruction count, offset +0x04
        buffer.extend(self.int_to_bytes(4, instruction_count))
        # add total param count, offset +0x08
        buffer.extend(self.int_to_bytes(4, param_count))
        # add version id, offset +0x0c
        buffer.extend(self.int_to_bytes(1, self.binary_metadata.version))
        # don't add instruction id byte size, always 1
        # add val byte size, offset +0x0d
        buffer.extend(self.int_to_bytes(1, self.binary_metadata.val_width))
        # add meta attribute count +0x0e
        buffer.extend(self.int_to_bytes(2, len(meta_attrs)))

        for key, value in meta_attrs.items():
            buffer.extend(self.str_to_bytes(key))
            buffer.extend(self.str_to_bytes(value))

        # add end pattern, offset +0x0e + meta attrs length
        buffer.extend(b'\x55')

        self.fp.write(buffer)

    def write_binary(self, instructions, meta_attrs):
        instruction_list = list(instructions)

        self.write_binary_metadata(instruction_list, meta_attrs)
        for instruction in instruction_list:
            self.write_instruction(instruction)

    def iid_to_bytes(self, bin_id):
        return self.int_to_bytes(self.binary_metadata.iid_width, bin_id)

    def val_to_bytes(self, val):
        return self.int_to_bytes(self.binary_metadata.val_width, val)

    def str_to_bytes(self, val):
        return bytes('{}\0'.format(val), encoding=self.encoding)


class BinaryMetadata:
    def __init__(self, signature, version,
                 iid_width=1, val_width=4, byte_order='be'):
        self.signature = BinaryMetadata.prepare_signature(signature)
        self.version = BinaryMetadata.prepare_version(version)
        self.iid_width = iid_width
        self.val_width = val_width
        self.byte_order = byte_order
        self.meta_attrs = {}

    def merge_meta_attrs(self, context):
        self.meta_attrs = { **self.meta_attrs, **context.defined_meta_attrs }

    @property
    def byte_order(self):
        return self._byte_order

    @byte_order.setter
    def byte_order(self, value):
        if value in ('le', 'be'):
            self._byte_order = value
        else:
            raise ValueError('invalid byte order specified')

    @staticmethod
    def prepare_signature(signature):
        if len(signature) >= 4:
            return signature[:4].upper()
        raise ValueError('signature metadata too short (expected 4 chars)')

    @staticmethod
    def prepare_version(version):
        if 0 < version < 256:
            return int(version)
        raise ValueError('version int too large (expected 1 byte)')
