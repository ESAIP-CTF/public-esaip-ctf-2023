using System;
using System.Collections.Generic;
using System.Threading;

namespace pwn_my_ship_1;


public class Chip8
{
    [Serializable]
    public class MemoryOverflow : Exception
    {
        public MemoryOverflow()
        {
        }

        public MemoryOverflow (string message)
            : base(message)
        {
        }
    }

    private class InvalidOpcode : Exception
    {

        public InvalidOpcode (ushort opcode)
            : base($"Opcode '0x{opcode:X4}' is invalid")
        {
        }
    }

    private class NoReturnAddress : Exception
    {
        public NoReturnAddress()
        : base("No return address on the stack")
        {
        }

    }

    private Dictionary<byte, Action<ushort>> _handlers;

    private string _borders;

    private const byte FontsetStartAdress = 0x0;
    private const int Width = 64, Height = 32;
        
    private Stack<ushort> _stack;
    private bool[] _keypad;

    private byte[] _memory;
    private byte[] _registers;
    private bool[] _gfx;

    private ushort _I;
    private ushort _PC;
    private byte _delayTimer;
    private byte _soundTimer;

    private Random _random;

    public Chip8(Random random, string opcodes, string flag)
    {
        byte[] font =
        {
            0xF0, 0x90, 0x90, 0x90, 0xF0, // 0 
            0x20, 0x60, 0x20, 0x20, 0x70, // 1 
            0xF0, 0x10, 0xF0, 0x80, 0xF0, // 2 
            0xF0, 0x10, 0xF0, 0x10, 0xF0, // 3 
            0x90, 0x90, 0xF0, 0x10, 0x10, // 4 
            0xF0, 0x80, 0xF0, 0x10, 0xF0, // 5 
            0xF0, 0x80, 0xF0, 0x90, 0xF0, // 6
            0xF0, 0x10, 0x20, 0x40, 0x40, // 7 
            0xF0, 0x90, 0xF0, 0x90, 0xF0, // 8 
            0xF0, 0x90, 0xF0, 0x10, 0xF0, // 9 
            0xF0, 0x90, 0xF0, 0x90, 0x90, // A 
            0xE0, 0x90, 0xE0, 0x90, 0xE0, // B 
            0xF0, 0x80, 0x80, 0x80, 0xF0, // C 
            0xE0, 0x90, 0x90, 0x90, 0xE0, // D 
            0xF0, 0x80, 0xF0, 0x80, 0xF0, // E 
            0xF0, 0x80, 0xF0, 0x80, 0x80 // F
        };

        _handlers = new Dictionary<byte, Action<ushort>>
        {
            { 0x0, Handle0 },
            { 0x1, Handle1 },
            { 0x2, Handle2 },
            { 0x3, Handle3 },
            { 0x4, Handle4 },
            { 0x5, Handle5 },
            { 0x6, Handle6 },
            { 0x7, Handle7 },
            { 0x8, Handle8 },
            { 0x9, Handle9 },
            { 0xA, HandleA },
            { 0xB, HandleB },
            { 0xC, HandleC },
            { 0xD, HandleD },
            { 0xE, HandleE },
            { 0xF, HandleF }
        };

        _stack = new Stack<ushort>();
        _keypad = new bool[0x10];
        _memory = new byte[0x1000];
        _registers = new byte[0x10];
        _gfx = new bool[32 * 64];

        _I = 0x0;
        _PC = 0x200;
        _delayTimer = 0x0;
        _soundTimer = 0x0;

        _random = random;

        for (var i = FontsetStartAdress; i < font.Length; i++)
            _memory[i] = font[i];

        for (var i = 0; i < flag.Length; i++)
            _memory[i + FontsetStartAdress + font.Length] = (byte)flag[i];

        if (opcodes.Length > _memory.Length - 0x200)
            throw new MemoryOverflow("Opcodes length must be smaller than 0x800");

        for (int i = 0; i < opcodes.Length; i++)
            _memory[0x200 + i] = (byte)opcodes[i];

        _borders = new string('-', 130);
    }

    private ushort this[int i] => (ushort)((_memory[i] << 8) + _memory[i + 1]);

    public void DebugMemory()
    {
        for (int i = 0x0; i < 0x1000; i += 0x10)
        {
            Console.Write("{0:X3}   ", i);
            for (int j = 0; j < 0x10; j++)
                Console.Write("{0:X2} ", _memory[i + j]);
                
            Console.WriteLine();
        }
    }

    private static byte GetN(ushort instruction)
    {
        return (byte)(instruction & 0xF);
    }

    private static byte GetNn(ushort instruction)
    {
        return (byte)(instruction & 0xFF);
    }
        
    private static ushort GetNnn(ushort instruction)
    {
        return (ushort)(instruction & 0xFFF);
    }
        
    private static byte GetX(ushort instruction)
    {
        return (byte)((instruction & 0xF00) >> 8);
    }
        
    private static byte GetY(ushort instruction)
    {
        return (byte)((instruction & 0xF0) >> 4);
    }
    
    private void Display(bool clearScreen)
    {
        if (clearScreen)
            for (var i = 0; i < _gfx.Length; i++)
                _gfx[i] = false;

        var output = _borders + "\n";

        for (var y = 0; y < 32; y++)
        {
            output += "|";
            
            for (var x = 0; x < 64; x++)
                output += _gfx[y * 64 + x] ? "██" : "  ";
            
            output += "|\n";
        }

        output += _borders;
        
        Console.WriteLine(output);
            
    }
    
    private bool ExecuteOp()
    {
        if (_PC >= _memory.Length)
            return false;
            
        ushort opcode = this[_PC];

        byte op = (byte)((opcode & 0xF000) >> 12);

        if (opcode == 0x0 || op == 1 && GetNnn(opcode) == _PC)
            return false;
            
        _PC += 0x2;

        try
        {
            _handlers[op](opcode);
            if (op == 0xD)
            {
                Console.Clear();
                Display(false);
            }
        }
        catch (KeyNotFoundException)
        {
            throw new InvalidOpcode(opcode);
        }


        return true;
    }

    public void Run()
    {
        Console.Clear();
        Display(false);

        while(ExecuteOp())
        {
            bool checkKey;
            try
            {
                checkKey = Console.KeyAvailable;
            }
            catch (Exception)
            {
                continue;
            }
            
            if (checkKey)
            {
                ConsoleKeyInfo key = Console.ReadKey(true);
                var index = key.Key switch
                {
                    ConsoleKey.D1 => 0x0,
                    ConsoleKey.D2 => 0x1,
                    ConsoleKey.D3 => 0x2,
                    ConsoleKey.D4 => 0x3,
                    ConsoleKey.Q => 0x4,
                    ConsoleKey.W => 0x5,
                    ConsoleKey.E => 0X6,
                    ConsoleKey.R => 0x7,
                    ConsoleKey.A => 0x8,
                    ConsoleKey.S => 0x9,
                    ConsoleKey.D => 0xA,
                    ConsoleKey.F => 0xB,
                    ConsoleKey.Z => 0xC,
                    ConsoleKey.X => 0xD,
                    ConsoleKey.C => 0xE,
                    ConsoleKey.V => 0xF,
                    _ => -1
                };

                if (index != -1)
                    _keypad[index] = true;
            }

            _delayTimer++;
            Thread.Sleep(8);
        }
    }
    
    private void Handle0(ushort opcode)
    {
        byte nn = GetNn(opcode);

        switch (nn)
        {
            case 0xEE when _stack.Count == 0:
                throw new NoReturnAddress();
            
            case 0xEE:
                _PC = _stack.Pop();
                break;
            
            case 0xE0:
                for (var i = 0; i < _gfx.Length; i++)
                    _gfx[i] = false;
                break;
            
            default:
                throw new InvalidOpcode(opcode);
        }
    }
    
    private void Handle1(ushort opcode)
    {
        _PC = GetNnn(opcode);
    }
    
    private void Handle2(ushort opcode)
    {
        _stack.Push(_PC);
        _PC = GetNnn(opcode);
    }
    
    private void Handle3(ushort opcode)
    {
        if (_registers[GetX(opcode)] == GetNn(opcode))
            _PC += 0x2;
    }
    
    private void Handle4(ushort opcode)
    {
        if (_registers[GetX(opcode)] != GetNn(opcode))
            _PC += 0x2;
    }
    
    private void Handle5(ushort opcode)
    {
        if (GetN(opcode) != 0)
            throw new InvalidOpcode(opcode);
        
        if (_registers[GetX(opcode)] == _registers[GetY(opcode)])
            _PC += 0x2;
    }
    
    private void Handle6(ushort opcode)
    {
        _registers[GetX(opcode)] = GetNn(opcode);
    }
    
    private void Handle7(ushort opcode)
    {
        _registers[GetX(opcode)] += GetNn(opcode);
    }
    
    private void Handle8(ushort opcode)
    {
        byte x = GetX(opcode);
        byte vx = _registers[x], vy = _registers[GetY(opcode)];
        int res;
            
        switch (GetN(opcode))
        {
            case 0x0:
                res = vy;
                break;
            case 0x1:
                res = vx | vy;
                break;
            case 0x2:
                res = vx & vy;
                break;
            case 0x3:
                res = vx ^ vy;
                break;
            case 0x4:
                int sum = vx + vy;
                    
                if (sum > 255)
                    _registers[0xf] = 1;
                else
                    _registers[0xf] = 0;

                res = sum & 0xFF;
                break;
            case 0x5:
                if (vx > vy)
                    _registers[0xf] = 1;
                else
                    _registers[0xf] = 0;
                res = vx - vy;
                break;
            case 0x6:
                res = vx >> 1;
                _registers[0xf] = GetN(vx);
                break;
            case 0x7:
                if (vy > vx)
                    _registers[0xf] = 1;
                else
                    _registers[0xf] = 0;
                res = vy - vx;
                break;
            case 0xE:
                res = vx << 1;
                _registers[0xf] = (byte)((_registers[x] & 0x80) >> 7);
                break;
            
            default:
                throw new InvalidOpcode(opcode);
            
        }

        _registers[x] = (byte)res;
    }
    
    private void Handle9(ushort opcode)
    {
        if (GetN(opcode) != 0)
            throw new InvalidOpcode(opcode);
        
        if (_registers[GetX(opcode)] != _registers[GetY(opcode)])
            _PC += 0x2;
    }
    
    private void HandleA(ushort opcode)
    {
        _I = GetNnn(opcode);
    }
    
    private void HandleB(ushort opcode)
    {
        _PC = (ushort)(GetNnn(opcode) + _registers[0x0]);
    }
    
    private void HandleC(ushort opcode)
    {
        _registers[GetX(opcode)] = (byte)(_random.Next(255) & GetNn(opcode));
    }
    
    private void HandleD(ushort opcode)
    {
        byte x = GetX(opcode);
        byte y = GetY(opcode);
        byte n = GetN(opcode);

        int xPos = _registers[x] % Width;
        int yPos = _registers[y] % Height;
        int startCoord = yPos * 64 + xPos;

        _registers[0xf] = 0;

        for (int row = 0; row < n; row++)
        {
            for (int col = 0; col < 8; col++)
            {
                int newCoord = startCoord + row * 64 + col;

                if (newCoord >= _gfx.Length)
                    continue;

                bool pixel = _gfx[newCoord] ^ true;

                if (_gfx[newCoord] && !pixel)
                    _registers[0xf] = 1;

                _gfx[newCoord] = pixel;
            }
        }
    }
    
    private void HandleE(ushort opcode)
    {
        byte nn = GetNn(opcode);
        byte vx = _registers[GetX(opcode)];
        
        switch (nn)
        {
            case 0x9E:
                if (_keypad[vx])
                    _PC += 0x2;
                break;
            
            case 0xA1:
                if (!_keypad[vx])
                    _PC += 0x2;
                break;
            
            default:
                throw new InvalidOpcode(opcode);
        }
    }
    
    private void HandleF(ushort opcode)
    {
        byte nn = GetNn(opcode);
        byte x = GetX(opcode);

        switch (nn)
        {
            case 0x07:
                _registers[x] = _delayTimer;
                break;
            
            case 0x0A:
                for (int i = 0; i < 0x10; i++)
                {
                    if (_keypad[i])
                    {
                        _registers[x] = (byte)i;
                        return;
                    }
                }

                _PC -= 0x2;
                break;
            
            case 0x15:
                _delayTimer = _registers[x];
                break;
            
            case 0x18:
                _soundTimer = _registers[x];
                break;
            
            case 0x1E:
                _I += _registers[x];
                break;
            
            case 0x29:
                _I = (ushort)(FontsetStartAdress + 5 * _registers[x]);
                break;
            
            case 0x33:
                int value = _registers[x];
                
                _memory[_I + 0x2] = (byte)(value % 10);
                value /= 10;

                _memory[_I + 0x1] = (byte)(value % 10);
                value /= 10;
                    
                _memory[_I] = (byte)(value % 10);
                break;
            
            case 0x55:
                for (int i = 0; i <= x; ++i)
                    _memory[_I + i] = _registers[i];
                break;
                
            case 0x65:
                for (int i = 0; i <= x; ++i)
                    _registers[i] = _memory[_I + i];
                break;
            
            default:
                throw new InvalidOpcode(opcode);
        }
    }
}
