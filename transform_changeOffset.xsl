<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:role="http://www.cs.rochester.edu/research/trips/role#"
    xmlns:TMA="http://www.cs.rochester.edu/research/trips/TMA#"
    xmlns:LF="http://www.cs.rochester.edu/research/trips/LF#"
    exclude-result-prefixes="xsl rdf role TMA LF">

<xsl:output method="xml" encoding="UTF-8" />

<xsl:template name="roles-to-attributes">
 <xsl:for-each select="*">
  <xsl:choose>
   <xsl:when test="@rdf:resource" /> <!-- these become elements -->
   <xsl:when test="self::LF:word">
    <xsl:attribute name="text">
     <xsl:value-of select="." />
    </xsl:attribute>
   </xsl:when>
   <xsl:otherwise>
    <xsl:attribute name="{local-name()}">
     <xsl:value-of select="." />
    </xsl:attribute>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:for-each>
</xsl:template>

<xsl:template name="roles-to-elements">
 <xsl:for-each select="role:*[@rdf:resource]">
  <xsl:text>
   </xsl:text>
  <RELATION
    id="{1 + count(preceding::role:*[@rdf:resource])}"
    head="{../@rdf:ID}"
    res="{substring(@rdf:resource,2)}"
    label="{local-name()}"
    />
 </xsl:for-each>
</xsl:template>

<xsl:template match="rdf:Description">
 <xsl:text>
   </xsl:text>
 <PHRASE id="{@rdf:ID}">
  <xsl:call-template name="roles-to-attributes" />
 </PHRASE>
 <xsl:call-template name="roles-to-elements" />
</xsl:template>

<xsl:template match="terms">
 <xsl:variable name="rootID" select="substring(@root,2)" />
 <xsl:text>
  </xsl:text>
 <SENTENCE id="s{1 + count(preceding::utt)}">
  <xsl:for-each select="rdf:RDF">
   <xsl:for-each select="rdf:Description[@rdf:ID = $rootID]">
    <xsl:call-template name="roles-to-attributes">
     <xsl:with-param name="descID" select="$rootID" />
    </xsl:call-template>
    <xsl:text>
   </xsl:text>
    <TEXT>
     <xsl:value-of select="substring(/trips-parser-output/@input, LF:start + 1, LF:end - LF:start)" />
    </TEXT>
    <xsl:call-template name="roles-to-elements" />
   </xsl:for-each>
   <xsl:apply-templates select="rdf:Description[@rdf:ID != $rootID]" />
  </xsl:for-each>
 <xsl:text>
  </xsl:text>
 </SENTENCE>
</xsl:template>

<xsl:template match="/trips-parser-output">
<SpRL><xsl:text>
 </xsl:text><SCENE>
  <xsl:apply-templates select="//utt/terms" /><xsl:text>
 </xsl:text></SCENE><xsl:text>
</xsl:text></SpRL>
</xsl:template>

</xsl:stylesheet>

