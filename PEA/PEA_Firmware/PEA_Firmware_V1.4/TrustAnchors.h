#pragma once
#include <SSLClient.h>
// Replace the following with your proxy/root CA certificate
extern const uint8_t TA_DER[] PROGMEM;
static const BearSSL::br_x509_trust_anchor TAs[] PROGMEM = {
    {
        NULL,  
        0,
        TA_DER,
        sizeof(TA_DER)
    }
};
static const size_t TAs_NUM = sizeof(TAs) / sizeof(TAs[0]);
