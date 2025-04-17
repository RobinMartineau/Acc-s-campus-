#include "pea.h"

Keypad4x4::Keypad4x4(const byte* rowPins,
                     const byte* colPins,
                     const char* keymap,
                     byte numRows,
                     byte numCols)
  : _rowPins(rowPins)
  , _colPins(colPins)
  , _keymap(keymap)
  , _numRows(numRows)
  , _numCols(numCols)
{}

void Keypad4x4::begin() {
  // Colonnes en INPUT_PULLUP, lignes en INPUT (ou flottant)
  for (byte c = 0; c < _numCols; c++) {
    pinMode(_colPins[c], INPUT_PULLUP);
  }
  for (byte r = 0; r < _numRows; r++) {
    pinMode(_rowPins[r], INPUT);
  }
}

char Keypad4x4::getKey() {
  for (byte r = 0; r < _numRows; r++) {
    // Active la ligne r
    setRowOutput(r);
    // Lis la colonne (0..numCols-1) qui passe à LOW
    int c = readColumns();
    if (c >= 0) {
      // Désactive la ligne avant de retourner
      pinMode(_rowPins[r], INPUT);
      return _keymap[r * _numCols + c];
    }
    // Désactive la ligne pour la prochaine itération
    pinMode(_rowPins[r], INPUT);
  }
  return 0;
}

void Keypad4x4::setRowOutput(byte row) {
  // Passe la ligne à LOW, les autres restent INPUT
  pinMode(_rowPins[row], OUTPUT);
  digitalWrite(_rowPins[row], LOW);
}

void Keypad4x4::setAllColumnsInputPullup() {
  for (byte c = 0; c < _numCols; c++) {
    pinMode(_colPins[c], INPUT_PULLUP);
  }
}

int Keypad4x4::readColumns() {
  // Si une colonne est à LOW, retourne son index
  for (byte c = 0; c < _numCols; c++) {
    if (digitalRead(_colPins[c]) == LOW) {
      // Attendre le relâchement pour débounce (optionnel)
      while (digitalRead(_colPins[c]) == LOW);
      delay(10);
      return c;
    }
  }
  return -1;
}
