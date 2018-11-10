<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:exsl="http://exslt.org/common"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:role="http://www.cs.rochester.edu/research/trips/role#"
    xmlns:TMA="http://www.cs.rochester.edu/research/trips/TMA#"
    xmlns:LF="http://www.cs.rochester.edu/research/trips/LF#"
    exclude-result-prefixes="xsl exsl rdf role TMA LF">

<xsl:output method="xml" encoding="UTF-8" />

<xsl:template name="roles-to-attributes-1">
 <!-- turn most child elements into attributes -->
 <xsl:for-each select="*">
  <xsl:choose>
   <xsl:when test="@rdf:resource" /> <!-- these become elements -->
   <xsl:when test="self::LF:word">
    <xsl:attribute name="word">
     <xsl:value-of select="." />
    </xsl:attribute>
   </xsl:when>
   <xsl:when test="self::LF:start | self::LF:end">
    <xsl:attribute name="phrase-{local-name()}">
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
 <!-- add lex-start/end by matching word tags with LF terms that have :LEX -->
 <xsl:if test="role:LEX and LF:indicator != 'SPEECHACT'">
  <xsl:variable name="phrase-id" select="@rdf:ID" />
  <xsl:variable name="phrase-start" select="number(LF:start)" />
  <xsl:variable name="phrase-end" select="number(LF:end)" />
  <xsl:variable name="lex" select="role:LEX" />
  <xsl:variable name="smaller-matching-phrases" select="../rdf:Description[@rdf:ID != $phrase-id and LF:indicator != 'SPEECHACT' and role:LEX = $lex and LF:start >= $phrase-start and $phrase-end >= LF:end]" />
  <xsl:variable name="tags" select="../../../tags" />
  <!-- for each word element that matches lex and fits inside the phrase
       (my kingdom for proper case folding functions in XPath...)  -->
  <xsl:variable name="words" select="$tags/word[translate(@lex, 'abcdefghijklmnopqrstuvwxyz ', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ-') = $lex and @start >= $phrase-start and $phrase-end >= @end]" />
  <xsl:for-each select="$words">
   <xsl:variable name="word-start" select="number(@start)" />
   <xsl:variable name="word-end" select="number(@end) + 1" />
   <!-- if no smaller matching phrase contains this word -->
   <xsl:if test="not($smaller-matching-phrases[$word-start >= LF:start and LF:end >= $word-end])">
    <!-- use the word's start/end as lex-start/end -->
    <xsl:attribute name="lex-start">
     <xsl:value-of select="$word-start" />
    </xsl:attribute>
    <xsl:attribute name="lex-end">
     <xsl:value-of select="$word-end" />
    </xsl:attribute>
   </xsl:if>
  </xsl:for-each>
 </xsl:if>
</xsl:template>

<xsl:template name="roles-to-attributes-2">
 <!-- pick which start/end to use -->
 <xsl:choose>
  <xsl:when test="@lex-start and @lex-end">
   <xsl:attribute name="start">
    <xsl:value-of select="@lex-start" />
   </xsl:attribute>
   <xsl:attribute name="end">
    <xsl:value-of select="@lex-end" />
   </xsl:attribute>
  </xsl:when>
  <xsl:when test="@phrase-start and @phrase-end">
   <xsl:attribute name="start">
    <xsl:value-of select="@phrase-start" />
   </xsl:attribute>
   <xsl:attribute name="end">
    <xsl:value-of select="@phrase-end" />
   </xsl:attribute>
  </xsl:when>
 </xsl:choose>
 <!-- copy over the other attributes -->
 <xsl:copy-of select="@*" />
</xsl:template>

<xsl:template name="roles-to-attributes-3">
 <xsl:choose>
  <!-- use start and end to get text when we have them -->
  <xsl:when test="@start and @end">
   <xsl:attribute name="text">
    <xsl:value-of select="substring(/attrs-2/input, @start + 1, @end - @start)" />
   </xsl:attribute>
  </xsl:when>
  <!-- include empty attributes for all three when we don't -->
  <xsl:otherwise>
   <xsl:attribute name="start" />
   <xsl:attribute name="end" />
   <xsl:attribute name="text" />
  </xsl:otherwise>
 </xsl:choose>
 <!-- copy over the other attributes -->
 <xsl:copy-of select="@*" />
</xsl:template>

<xsl:template name="roles-to-attributes">
 <!-- process attrs in 3 stages -->
 <xsl:variable name="attrs-1">
  <attrs-1>
   <xsl:call-template name="roles-to-attributes-1" />
  </attrs-1>
 </xsl:variable>
 <xsl:variable name="attrs-2">
  <attrs-2>
   <xsl:for-each select="exsl:node-set($attrs-1)/*">
    <xsl:call-template name="roles-to-attributes-2" />
   </xsl:for-each>
   <!-- need to propagate this into roles-to-attributes-3 -->
   <input><xsl:value-of select="/trips-parser-output/@input" /></input>
  </attrs-2>
 </xsl:variable>
 <xsl:for-each select="exsl:node-set($attrs-2)/*">
  <xsl:call-template name="roles-to-attributes-3" />
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
    <xsl:call-template name="roles-to-attributes" />
    <xsl:text>
   </xsl:text>
    <TEXT>
     <xsl:value-of select="substring(/trips-parser-output/@input, LF:start + 1, LF:end - LF:start + 1)" />
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
<CleanedXML>
  <xsl:apply-templates select="//utt/terms" /><xsl:text>
 </xsl:text></CleanedXML>
</xsl:template>

</xsl:stylesheet>

